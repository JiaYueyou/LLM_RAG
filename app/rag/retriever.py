# 向量检索器

import os
from typing import List, Dict, Any

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from config import Config

class VectorRetriever:
    def __init__(self):
        """初始化向量检索器"""
        self.embeddings = OpenAIEmbeddings(
            model=Config.EMBEDDING_MODEL_NAME,
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
        
        # 确保向量数据库目录存在
        os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
        
        # 初始化向量数据库
        self._init_db()
    
    def _init_db(self):
        """初始化向量数据库"""
        try:
            # 检查是否已有数据库
            if os.path.exists(os.path.join(Config.VECTOR_DB_PATH, "chroma.sqlite3")):
                print("加载已存在的向量数据库")
                self.db = Chroma(
                    persist_directory=Config.VECTOR_DB_PATH,
                    embedding_function=self.embeddings
                )
            else:
                print("未找到已存在的向量数据库，将创建新的数据库")
                self.db = Chroma(
                    persist_directory=Config.VECTOR_DB_PATH,
                    embedding_function=self.embeddings
                )
        except Exception as e:
            print(f"初始化向量数据库失败: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """
        添加文档到向量数据库

        documents: 文档列表
        returns: 添加结果
        """
        try:
            # 添加文档
            self.db.add_documents(documents)
            print(f"成功添加 {len(documents)} 个文档到向量数据库")
            
            return {
                "success": True,
                "count": len(documents)
            }
            
        except Exception as e:
            print(f"添加文档失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "count": 0
            }
    
    def as_retriever(self, search_type: str = "similarity", k: int = Config.RETRIEVAL_K):
        """
        获取检索器
        
        search_type: 搜索类型
        k: 返回文档数量
            
        returns: 检索器对象
        """
        return self.db.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )
    
    def search(self, query: str, k: int = Config.RETRIEVAL_K) -> List[Document]:
        """
        搜索相关文档

        query: 查询字符串
        k: 返回文档数量
            
        returns: 相关文档列表
        """
        try:
            retriever = self.as_retriever(k=k)
            docs = retriever.invoke(query)
            return docs
        except Exception as e:
            print(f"搜索失败: {str(e)}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        获取集合信息
        
        returns: 集合信息
        """
        try:
            count = self.db._collection.count()
            return {
                "success": True,
                "count": count,
                "name": self.db._collection.name
            }
        except Exception as e:
            print(f"获取集合信息失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "count": 0
            }
    
    def clear_collection(self) -> Dict[str, Any]:
        """
        清空集合
        
        returns: 清空结果
        """
        try:
            # 删除集合
            self.db.delete_collection()
            
            # 重新初始化
            self._init_db()
            
            return {
                "success": True,
                "message": "向量数据库已清空"
            }
        except Exception as e:
            print(f"清空集合失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }