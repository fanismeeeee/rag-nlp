import os

class Config:
    """Configuration class for the RAG knowledge base project."""
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DOCS_DIR = os.path.join(BASE_DIR, 'docs')
    DB_DIR = os.path.join(BASE_DIR, 'db')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    
    # Model configuration
    LOCAL_MODEL_PATH = os.path.join(MODELS_DIR, 'local_model')  # Adjust as necessary
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Vector store configuration
    VECTOR_STORE_PERSIST_DIR = DB_DIR
    
    # Other configurations
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    LLM_TEMPERATURE = 0.7
    
    @staticmethod
    def print_config():
        """Print the current configuration."""
        print("Current Configuration:")
        print(f"BASE_DIR: {Config.BASE_DIR}")
        print(f"DOCS_DIR: {Config.DOCS_DIR}")
        print(f"DB_DIR: {Config.DB_DIR}")
        print(f"MODELS_DIR: {Config.MODELS_DIR}")
        print(f"LOCAL_MODEL_PATH: {Config.LOCAL_MODEL_PATH}")
        print(f"EMBEDDING_MODEL_NAME: {Config.EMBEDDING_MODEL_NAME}")
        print(f"VECTOR_STORE_PERSIST_DIR: {Config.VECTOR_STORE_PERSIST_DIR}")
        print(f"CHUNK_SIZE: {Config.CHUNK_SIZE}")
        print(f"CHUNK_OVERLAP: {Config.CHUNK_OVERLAP}")
        print(f"LLM_TEMPERATURE: {Config.LLM_TEMPERATURE}")