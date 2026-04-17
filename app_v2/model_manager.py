"""
Lazy-loading model manager with LRU caching.
Reduces memory usage by loading embedding models on-demand.
"""
import gc
from typing import Any, Dict, Optional
from collections import OrderedDict

from data_loader import EmbeddingLibrary
from recommender import MusicRecommender


class ModelManager:
    """
    Manages embedding models with lazy-loading and LRU eviction.
    
    Instead of loading all 9 models at startup (~670MB), only loads
    models when requested and keeps at most `max_cached_models` in memory.
    """
    
    def __init__(self, embedding_library: EmbeddingLibrary, max_cached_models: int = 2):
        self.embedding_library = embedding_library
        self.recommenders: Dict[str, MusicRecommender] = {}
        self.max_cached_models = max_cached_models
        self.access_order: OrderedDict = OrderedDict()
    
    def get_recommender(self, model_name: str) -> MusicRecommender:
        """
        Get or create a recommender for the specified model.
        
        Uses LRU (Least Recently Used) eviction when at capacity.
        
        Args:
            model_name: Display name of the embedding model (e.g., 'MiniLM', 'MPNet')
        
        Returns:
            MusicRecommender instance for the requested model
        """
        # If already loaded, move to end of access order (most recently used)
        if model_name in self.recommenders:
            self.access_order.move_to_end(model_name)
            return self.recommenders[model_name]
        
        # Evict LRU model if at capacity
        if len(self.recommenders) >= self.max_cached_models:
            self._evict_lru()
        
        # Load model on-demand
        embeddings = self.embedding_library.get_embeddings(model_name)
        recommender = MusicRecommender(self.embedding_library.df, embeddings)
        
        self.recommenders[model_name] = recommender
        self.access_order[model_name] = None  # Just tracking access order
        
        return recommender
    
    def _evict_lru(self):
        """Evict the least recently used model from memory."""
        if not self.access_order:
            return
        
        # Get oldest (least recently used) model
        lru_model = next(iter(self.access_order))
        
        # Remove from tracking and recommenders
        del self.access_order[lru_model]
        del self.recommenders[lru_model]
        
        # Force garbage collection to free memory immediately
        gc.collect()
    
    def get_available_models(self) -> list:
        """Get list of available model names."""
        return list(self.embedding_library.embeddings_dict.keys())
    
    def get_default_model(self) -> str:
        """Get the default model name (MiniLM if available, else first available)."""
        models = self.get_available_models()
        return "MiniLM" if "MiniLM" in models else (models[0] if models else None)
    
    def clear_cache(self):
        """Clear all cached models (useful for testing or manual memory management)."""
        self.recommenders.clear()
        self.access_order.clear()
        gc.collect()
