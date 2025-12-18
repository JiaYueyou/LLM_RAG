# 文档加载器 支持PDF, TXT, DOCX, Markdown

import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config

class DocumentLoader:
    def __init__(self):
        """初始化文档加载器"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
    
    def load_single_document(self, file_path: str):
        """
        加载单个文档
        
        file_path: 文档路径
            
        returns: 文档块列表
        """
        try:
            # 根据文件扩展名选择合适的加载器
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_ext in ['.docx', '.doc']:
                loader = Docx2txtLoader(file_path)
            elif file_ext in ['.md', '.markdown']:
                loader = UnstructuredMarkdownLoader(file_path, encoding='utf-8')
            else:
                print(f"不支持的文件格式: {file_ext}")
                return []
            
            # 加载文档
            documents = loader.load()
            
            # 分割文档
            chunks = self.text_splitter.split_documents(documents)
            print(f"文件 {os.path.basename(file_path)} 已加载并分割为 {len(chunks)} 个文本块")
            
            return chunks
            
        except Exception as e:
            print(f"加载文档失败 {file_path}: {str(e)}")
            return []
    
    def load_directory(self, directory_path: str):
        """
        加载目录中的所有文档
        
        directory_path: 目录路径
            
        returns: 所有文档的文本块列表
        """
        all_chunks = []
        
        # 支持的文件扩展名
        supported_extensions = ['.txt', '.md', '.pdf', '.docx', '.doc',]
        
        # 遍历目录中的文件
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in supported_extensions:
                    chunks = self.load_single_document(file_path)
                    all_chunks.extend(chunks)
        
        return all_chunks