"""
数据插入脚本，将docs目录下的所有文档加载并存储到向量数据库中
"""

import os
from app.data.loader import DocumentLoader
from app.rag.retriever import VectorRetriever


def main():
    """主函数，直接处理docs目录下的所有文件"""
    # 设置docs目录路径
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs")
    
    print(f"正在处理目录: {docs_dir}")
    
    # 检查目录是否存在
    if not os.path.exists(docs_dir):
        print(f"错误: docs目录不存在: {docs_dir}")
        return
    
    # 初始化加载器和检索器
    loader = DocumentLoader()
    retriever = VectorRetriever()
    
    # 加载目录中的所有文档
    documents = loader.load_directory(docs_dir)
    
    if not documents:
        print("目录中没有找到支持的文件")
        return
    
    print(f"共加载了 {len(documents)} 个文档块")
    
    # 存储到向量数据库
    result = retriever.add_documents(documents)
    
    if result["success"]:
        print(f"成功存储所有文档到向量数据库")
    else:
        print(f"存储文档失败")


if __name__ == "__main__":
    main()