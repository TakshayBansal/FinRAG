"""
RAPTOR-style clustering implementation for FinRAG.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.mixture import GaussianMixture
import umap
from dataclasses import dataclass


@dataclass
class ClusterNode:
    """Represents a node in the RAPTOR tree."""
    node_id: str
    text: str
    embedding: np.ndarray
    children: List['ClusterNode']
    level: int
    metadata: Dict[str, Any]


class RAPTORClustering:
    """
    Implements RAPTOR's clustering algorithm for building hierarchical tree structures.
    """
    
    def __init__(
        self,
        max_cluster_size: int = 100,
        min_cluster_size: int = 5,
        reduction_dimension: int = 10,
        clustering_algorithm: str = "gaussian_mixture"
    ):
        self.max_cluster_size = max_cluster_size
        self.min_cluster_size = min_cluster_size
        self.reduction_dimension = reduction_dimension
        self.clustering_algorithm = clustering_algorithm
    
    def global_cluster_embeddings(
        self,
        embeddings: np.ndarray,
        dim: int = None,
        n_neighbors: Optional[int] = None,
        metric: str = "cosine"
    ) -> np.ndarray:
        """
        Perform global dimensionality reduction on embeddings using UMAP.
        
        Args:
            embeddings: Input embeddings
            dim: Target dimension (default: self.reduction_dimension)
            n_neighbors: Number of neighbors for UMAP
            metric: Distance metric
        
        Returns:
            Reduced embeddings
        """
        if dim is None:
            dim = self.reduction_dimension
        
        if n_neighbors is None:
            n_neighbors = int((len(embeddings) - 1) ** 0.5)
        
        reducer = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=min(dim, len(embeddings) - 2),
            metric=metric,
            random_state=42
        )
        
        return reducer.fit_transform(embeddings)
    
    def local_cluster_embeddings(
        self,
        embeddings: np.ndarray,
        dim: int = None,
        num_neighbors: int = 10,
        metric: str = "cosine"
    ) -> np.ndarray:
        """
        Perform local dimensionality reduction on embeddings using UMAP.
        
        Args:
            embeddings: Input embeddings
            dim: Target dimension
            num_neighbors: Number of neighbors
            metric: Distance metric
        
        Returns:
            Reduced embeddings
        """
        if dim is None:
            dim = self.reduction_dimension
        
        reducer = umap.UMAP(
            n_neighbors=num_neighbors,
            n_components=min(dim, len(embeddings) - 2),
            metric=metric,
            random_state=42
        )
        
        return reducer.fit_transform(embeddings)
    
    def get_optimal_clusters(
        self,
        embeddings: np.ndarray,
        max_clusters: int = 50,
        random_state: int = 42
    ) -> int:
        """
        Determine optimal number of clusters using BIC for Gaussian Mixture Models.
        
        Args:
            embeddings: Input embeddings
            max_clusters: Maximum number of clusters to try
            random_state: Random state for reproducibility
        
        Returns:
            Optimal number of clusters
        """
        max_clusters = min(max_clusters, len(embeddings))
        n_clusters = np.arange(1, max_clusters)
        bics = []
        
        for n in n_clusters:
            gm = GaussianMixture(n_components=n, random_state=random_state)
            gm.fit(embeddings)
            bics.append(gm.bic(embeddings))
        
        # Find elbow point
        optimal_clusters = n_clusters[np.argmin(bics)]
        return optimal_clusters
    
    def gmm_clustering(
        self,
        embeddings: np.ndarray,
        threshold: float = 0.5,
        random_state: int = 42
    ) -> List[np.ndarray]:
        """
        Perform Gaussian Mixture Model clustering.
        
        Args:
            embeddings: Input embeddings
            threshold: Probability threshold for cluster assignment
            random_state: Random state
        
        Returns:
            List of clusters (each cluster is an array of indices)
        """
        n_clusters = self.get_optimal_clusters(embeddings)
        gm = GaussianMixture(n_components=n_clusters, random_state=random_state)
        gm.fit(embeddings)
        
        probs = gm.predict_proba(embeddings)
        labels = [np.where(prob > threshold)[0] for prob in probs]
        
        # Group by cluster
        clusters = [[] for _ in range(n_clusters)]
        for idx, label_list in enumerate(labels):
            for label in label_list:
                clusters[label].append(idx)
        
        # Filter out empty clusters and convert to numpy arrays
        clusters = [np.array(cluster) for cluster in clusters if len(cluster) > 0]
        
        return clusters
    
    def perform_clustering(
        self,
        embeddings: np.ndarray,
        dim: int = 10,
        threshold: float = 0.5
    ) -> List[np.ndarray]:
        """
        Perform the full clustering pipeline: reduction + clustering.
        
        Args:
            embeddings: Input embeddings
            dim: Dimension for reduction
            threshold: Clustering threshold
        
        Returns:
            List of clusters
        """
        if len(embeddings) <= self.min_cluster_size:
            # Don't cluster if too few items
            return [np.arange(len(embeddings))]
        
        # Reduce dimensionality
        reduced_embeddings = self.global_cluster_embeddings(embeddings, dim=dim)
        
        # Perform clustering
        if self.clustering_algorithm == "gaussian_mixture":
            clusters = self.gmm_clustering(reduced_embeddings, threshold=threshold)
        elif self.clustering_algorithm == "kmeans":
            n_clusters = min(len(embeddings) // self.min_cluster_size, 10)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            labels = kmeans.fit_predict(reduced_embeddings)
            clusters = [np.where(labels == i)[0] for i in range(n_clusters)]
        else:
            raise ValueError(f"Unknown clustering algorithm: {self.clustering_algorithm}")
        
        # Filter clusters by size
        clusters = [
            cluster for cluster in clusters 
            if len(cluster) >= self.min_cluster_size
        ]
        
        return clusters
