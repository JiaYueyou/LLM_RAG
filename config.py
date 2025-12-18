import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # 模型名称，默认为gpt-3.5-turbo
    MODEL_NAME = OPENAI_MODEL
    TEMPERATURE = 0.5
    
    # 向量数据库配置
    VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "chromadb")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
    
    # RAG配置
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))  # 自定义文档存储时的分块大小
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))  # 自定义文档存储时的分块重叠大小（一般为块大小的1/5）
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))
    
    # 应用配置
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")