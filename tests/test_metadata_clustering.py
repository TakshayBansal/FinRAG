"""
Unit tests for metadata clustering functionality in FinRAG.

Tests cover:
- Metadata extraction from financial documents
- Metadata-based grouping
- Two-stage clustering process
- Integration with RAPTOR tree
"""

import unittest
from finrag.models import FinancialChunker
from finrag.core.clustering import RAPTORClustering
from finrag.core.clustering import ClusterNode
from finrag.models import OpenAIEmbeddingModel
from finrag.config import FinRAGConfig
import numpy as np


class TestMetadataExtraction(unittest.TestCase):
    """Test metadata extraction from documents."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.chunker = FinancialChunker(chunk_size=1000, chunk_overlap=200)
    
    def test_extract_year(self):
        """Test year extraction."""
        text = "Apple Inc. 2023 Annual Report shows strong growth in 2023."
        metadata = self.chunker.extract_metadata(text)
        self.assertEqual(metadata.get('year'), '2023')
    
    def test_extract_company_inc(self):
        """Test company extraction with Inc suffix."""
        text = "Apple Inc. released their quarterly earnings."
        metadata = self.chunker.extract_metadata(text)
        self.assertEqual(metadata.get('company'), 'Apple Inc.')
    
    def test_extract_company_corp(self):
        """Test company extraction with Corp suffix."""
        text = "JPMorgan Chase & Co. reported strong results."
        metadata = self.chunker.extract_metadata(text)
        self.assertIn('JPMorgan', metadata.get('company', ''))
    
    def test_extract_sector_finance(self):
        """Test finance sector extraction."""
        text = "This finance sector report covers banking operations."
        metadata = self.chunker.extract_metadata(text)
        self.assertEqual(metadata.get('sector'), 'finance')
    
    def test_extract_sector_technology(self):
        """Test technology sector extraction."""
        text = "Apple Inc. technology sector innovations in 2023."
        metadata = self.chunker.extract_metadata(text)
        self.assertEqual(metadata.get('sector'), 'technology')
    
    def test_extract_all_metadata(self):
        """Test extraction of all metadata fields."""
        text = """
        JPMorgan Chase & Co. 2023 Annual Report - Finance Sector
        
        Financial performance for the finance sector leader.
        """
        metadata = self.chunker.extract_metadata(text)
        
        self.assertIsNotNone(metadata.get('year'))
        self.assertIsNotNone(metadata.get('company'))
        self.assertIsNotNone(metadata.get('sector'))
    
    def test_missing_metadata(self):
        """Test handling of missing metadata."""
        text = "This is a generic document with no specific metadata."
        metadata = self.chunker.extract_metadata(text)
        
        # Should return empty dict or None for missing fields
        self.assertIsInstance(metadata, dict)
    
    def test_chunk_with_metadata(self):
        """Test that chunks include metadata."""
        text = """
        Apple Inc. 2023 Annual Report - Technology Sector
        
        This is a long document that will be split into multiple chunks.
        """ * 10  # Make it long enough to create multiple chunks
        
        chunks = self.chunker.chunk_text_with_metadata(text)
        
        # All chunks should have metadata
        for chunk in chunks:
            self.assertIn('metadata', chunk)
            metadata = chunk['metadata']
            self.assertIsInstance(metadata, dict)


class TestMetadataClustering(unittest.TestCase):
    """Test metadata-based clustering functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = FinRAGConfig()
        self.embedding_model = OpenAIEmbeddingModel()
        self.clustering = RAPTORClustering(
            reduction_dimension=10,
            max_clusters=5,
            use_metadata_clustering=True,
            metadata_keys=['sector', 'company', 'year']
        )
    
    def test_extract_metadata_groups(self):
        """Test grouping nodes by metadata."""
        # Create test nodes with different metadata
        nodes = [
            ClusterNode(
                text="JPMorgan doc 1",
                index=0,
                metadata={'sector': 'finance', 'company': 'JPMorgan', 'year': '2023'}
            ),
            ClusterNode(
                text="JPMorgan doc 2",
                index=1,
                metadata={'sector': 'finance', 'company': 'JPMorgan', 'year': '2023'}
            ),
            ClusterNode(
                text="Apple doc 1",
                index=2,
                metadata={'sector': 'technology', 'company': 'Apple', 'year': '2023'}
            ),
        ]
        
        groups = self.clustering.extract_metadata_groups(nodes)
        
        # Should have 2 groups
        self.assertEqual(len(groups), 2)
        
        # Check group sizes
        jpmorgan_key = ('finance', 'JPMorgan', '2023')
        apple_key = ('technology', 'Apple', '2023')
        
        self.assertEqual(len(groups[jpmorgan_key]), 2)
        self.assertEqual(len(groups[apple_key]), 1)
    
    def test_metadata_clustering_with_nodes(self):
        """Test full metadata clustering process."""
        # Create test nodes
        nodes = []
        embeddings_list = []
        
        # JPMorgan group
        for i in range(5):
            nodes.append(ClusterNode(
                text=f"JPMorgan doc {i}",
                index=i,
                metadata={'sector': 'finance', 'company': 'JPMorgan', 'year': '2023'}
            ))
            embeddings_list.append(np.random.randn(1536))  # OpenAI embedding dimension
        
        # Apple group
        for i in range(5, 10):
            nodes.append(ClusterNode(
                text=f"Apple doc {i}",
                index=i,
                metadata={'sector': 'technology', 'company': 'Apple', 'year': '2023'}
            ))
            embeddings_list.append(np.random.randn(1536))
        
        embeddings = np.array(embeddings_list)
        
        # Perform metadata clustering
        clusters = self.clustering.perform_clustering_with_nodes(nodes, embeddings)
        
        # Should return clusters
        self.assertIsInstance(clusters, list)
        self.assertGreater(len(clusters), 0)
    
    def test_standard_clustering_fallback(self):
        """Test fallback to standard clustering when metadata clustering disabled."""
        clustering_no_metadata = RAPTORClustering(
            reduction_dimension=10,
            max_clusters=5,
            use_metadata_clustering=False
        )
        
        # Create nodes without metadata
        nodes = [
            ClusterNode(text=f"Doc {i}", index=i, metadata={})
            for i in range(10)
        ]
        embeddings = np.random.randn(10, 1536)
        
        # Should use standard clustering
        clusters = clustering_no_metadata.perform_clustering_with_nodes(nodes, embeddings)
        
        self.assertIsInstance(clusters, list)


class TestMetadataIntegration(unittest.TestCase):
    """Integration tests for metadata clustering with FinRAG."""
    
    def test_metadata_in_config(self):
        """Test metadata configuration."""
        config = FinRAGConfig()
        
        # Check default values
        self.assertTrue(config.use_metadata_clustering)
        self.assertEqual(config.metadata_keys, ["sector", "company", "year"])
    
    def test_custom_metadata_keys(self):
        """Test custom metadata keys."""
        config = FinRAGConfig()
        config.metadata_keys = ["sector", "year"]
        
        self.assertEqual(len(config.metadata_keys), 2)
        self.assertIn("sector", config.metadata_keys)
        self.assertIn("year", config.metadata_keys)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.chunker = FinancialChunker(chunk_size=1000, chunk_overlap=200)
        self.clustering = RAPTORClustering(
            reduction_dimension=10,
            max_clusters=5,
            use_metadata_clustering=True
        )
    
    def test_empty_document(self):
        """Test handling of empty document."""
        chunks = self.chunker.chunk_text_with_metadata("")
        self.assertEqual(len(chunks), 0)
    
    def test_no_metadata_in_document(self):
        """Test document with no extractable metadata."""
        text = "This is a generic document."
        chunks = self.chunker.chunk_text_with_metadata(text)
        
        for chunk in chunks:
            self.assertIn('metadata', chunk)
            # Metadata might be empty dict
            self.assertIsInstance(chunk['metadata'], dict)
    
    def test_partial_metadata(self):
        """Test document with only partial metadata."""
        text = "Apple Inc. released new products."  # Has company, no year/sector
        metadata = self.chunker.extract_metadata(text)
        
        # Should extract at least company
        self.assertIn('company', metadata)
    
    def test_multiple_years(self):
        """Test document with multiple years."""
        text = "Comparing 2022 and 2023 performance."
        metadata = self.chunker.extract_metadata(text)
        
        # Should extract one of the years
        if 'year' in metadata:
            self.assertIn(metadata['year'], ['2022', '2023'])
    
    def test_single_node_cluster(self):
        """Test clustering with single node."""
        nodes = [
            ClusterNode(
                text="Single doc",
                index=0,
                metadata={'sector': 'finance', 'company': 'Test', 'year': '2023'}
            )
        ]
        embeddings = np.random.randn(1, 1536)
        
        # Should handle gracefully
        clusters = self.clustering.perform_clustering_with_nodes(nodes, embeddings)
        self.assertIsInstance(clusters, list)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMetadataExtraction))
    suite.addTests(loader.loadTestsFromTestCase(TestMetadataClustering))
    suite.addTests(loader.loadTestsFromTestCase(TestMetadataIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
