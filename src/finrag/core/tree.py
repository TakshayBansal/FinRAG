"""
RAPTOR Tree implementation for hierarchical document organization.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass, asdict
import json
import pickle
from pathlib import Path

from .clustering import RAPTORClustering, ClusterNode
from .base_models import BaseEmbeddingModel, BaseSummarizationModel


@dataclass
class TreeConfig:
    """Configuration for RAPTOR tree building."""
    max_depth: int = 3
    max_cluster_size: int = 100
    min_cluster_size: int = 5
    reduction_dimension: int = 10
    summarization_length: int = 200


class RAPTORTree:
    """
    Implements the RAPTOR tree structure for hierarchical document organization.
    """
    
    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
        summarization_model: BaseSummarizationModel,
        config: TreeConfig = None
    ):
        self.embedding_model = embedding_model
        self.summarization_model = summarization_model
        self.config = config or TreeConfig()
        self.clustering = RAPTORClustering(
            max_cluster_size=self.config.max_cluster_size,
            min_cluster_size=self.config.min_cluster_size,
            reduction_dimension=self.config.reduction_dimension
        )
        
        self.root_nodes: List[ClusterNode] = []
        self.all_nodes: Dict[str, ClusterNode] = {}
        self.leaf_nodes: List[ClusterNode] = []
    
    def build_tree(
        self,
        chunks: List[Dict[str, Any]],
        chunk_embeddings: np.ndarray
    ) -> None:
        """
        Build the RAPTOR tree from document chunks.
        
        Args:
            chunks: List of document chunks with metadata
            chunk_embeddings: Embeddings for each chunk
        """
        # Initialize leaf nodes
        self.leaf_nodes = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
            node = ClusterNode(
                node_id=f"leaf_{idx}",
                text=chunk["text"],
                embedding=embedding,
                children=[],
                level=0,
                metadata=chunk
            )
            self.leaf_nodes.append(node)
            self.all_nodes[node.node_id] = node
        
        # Build tree recursively
        current_level_nodes = self.leaf_nodes
        current_level = 0
        
        print(f"Level 0 (leaves): {len(current_level_nodes)} nodes")
        
        while current_level < self.config.max_depth and len(current_level_nodes) > 1:
            print(f"Building level {current_level + 1}...")
            next_level_nodes = self._build_level(
                current_level_nodes,
                current_level + 1
            )
            
            if len(next_level_nodes) == 0:
                break
            
            print(f"Level {current_level + 1}: {len(next_level_nodes)} nodes")
            current_level_nodes = next_level_nodes
            current_level += 1
        
        # Set root nodes
        self.root_nodes = current_level_nodes
        print(f"Tree building complete! Total levels: {current_level + 1}")
    
    def _build_level(
        self,
        nodes: List[ClusterNode],
        level: int
    ) -> List[ClusterNode]:
        """
        Build a single level of the tree.
        
        Args:
            nodes: Nodes from the previous level
            level: Current level number
        
        Returns:
            New nodes for this level
        """
        if len(nodes) <= self.config.min_cluster_size:
            return []
        
        # Get embeddings for current nodes
        embeddings = np.array([node.embedding for node in nodes])
        
        # Perform clustering
        clusters = self.clustering.perform_clustering(embeddings)
        
        if len(clusters) == 0:
            return []
        
        # Create parent nodes for each cluster
        new_nodes = []
        total_clusters = len(clusters)
        print(f"  Creating {total_clusters} cluster summaries...")
        
        for cluster_idx, cluster in enumerate(clusters):
            cluster_nodes = [nodes[i] for i in cluster]
            
            # Progress indicator
            if (cluster_idx + 1) % 5 == 0 or cluster_idx == total_clusters - 1:
                print(f"  Progress: {cluster_idx + 1}/{total_clusters} clusters processed")
            
            # Summarize cluster
            cluster_texts = [node.text for node in cluster_nodes]
            summary = self.summarization_model.summarize(
                cluster_texts,
                max_tokens=self.config.summarization_length
            )
            
            # Create embedding for summary
            summary_embedding = self.embedding_model.create_embedding(summary)
            
            # Create new parent node
            parent_node = ClusterNode(
                node_id=f"level_{level}_cluster_{cluster_idx}",
                text=summary,
                embedding=summary_embedding,
                children=cluster_nodes,
                level=level,
                metadata={
                    "num_children": len(cluster_nodes),
                    "cluster_idx": cluster_idx
                }
            )
            
            new_nodes.append(parent_node)
            self.all_nodes[parent_node.node_id] = parent_node
        
        return new_nodes
    
    def save(self, path: str) -> None:
        """Save the tree to disk."""
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Save tree structure
        tree_data = {
            "config": asdict(self.config),
            "root_node_ids": [node.node_id for node in self.root_nodes],
            "leaf_node_ids": [node.node_id for node in self.leaf_nodes],
            "all_nodes": {}
        }
        
        # Serialize nodes
        for node_id, node in self.all_nodes.items():
            tree_data["all_nodes"][node_id] = {
                "node_id": node.node_id,
                "text": node.text,
                "embedding": node.embedding.tolist(),
                "children_ids": [child.node_id for child in node.children],
                "level": node.level,
                "metadata": node.metadata
            }
        
        # Save as JSON and pickle
        with open(save_path / "tree.json", "w") as f:
            json.dump(tree_data, f, indent=2)
        
        with open(save_path / "tree.pkl", "wb") as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, path: str, embedding_model: BaseEmbeddingModel, 
             summarization_model: BaseSummarizationModel) -> 'RAPTORTree':
        """Load a tree from disk."""
        load_path = Path(path)
        
        # Try pickle first (fastest)
        pkl_path = load_path / "tree.pkl"
        if pkl_path.exists():
            with open(pkl_path, "rb") as f:
                tree = pickle.load(f)
                tree.embedding_model = embedding_model
                tree.summarization_model = summarization_model
                return tree
        
        # Fall back to JSON
        json_path = load_path / "tree.json"
        with open(json_path, "r") as f:
            tree_data = json.load(f)
        
        # Reconstruct tree
        config = TreeConfig(**tree_data["config"])
        tree = cls(embedding_model, summarization_model, config)
        
        # Rebuild nodes
        all_nodes = {}
        for node_id, node_data in tree_data["all_nodes"].items():
            node = ClusterNode(
                node_id=node_data["node_id"],
                text=node_data["text"],
                embedding=np.array(node_data["embedding"]),
                children=[],  # Will be filled later
                level=node_data["level"],
                metadata=node_data["metadata"]
            )
            all_nodes[node_id] = node
        
        # Rebuild parent-child relationships
        for node_id, node_data in tree_data["all_nodes"].items():
            node = all_nodes[node_id]
            node.children = [all_nodes[child_id] for child_id in node_data["children_ids"]]
        
        tree.all_nodes = all_nodes
        tree.root_nodes = [all_nodes[node_id] for node_id in tree_data["root_node_ids"]]
        tree.leaf_nodes = [all_nodes[node_id] for node_id in tree_data["leaf_node_ids"]]
        
        return tree
    
    def get_all_texts(self) -> List[str]:
        """Get all texts in the tree."""
        return [node.text for node in self.all_nodes.values()]
    
    def get_all_embeddings(self) -> np.ndarray:
        """Get all embeddings in the tree."""
        return np.array([node.embedding for node in self.all_nodes.values()])
    
    def get_node_by_id(self, node_id: str) -> Optional[ClusterNode]:
        """Get a node by its ID."""
        return self.all_nodes.get(node_id)
