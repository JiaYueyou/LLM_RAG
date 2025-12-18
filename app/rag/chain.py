# RAG链

from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from config import Config
from .retriever import VectorRetriever

class RAGChain:
    def __init__(self):
        """初始化RAG链"""
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=0.5,
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
        
        self.retriever = VectorRetriever()
        
        # 定义提示模板
        self.prompt = ChatPromptTemplate.from_template("""
                基于以下上下文回答问题。如果上下文中没有相关信息，请说"根据提供的上下文，我无法回答这个问题"。

                上下文：
                {context}

                问题：{question}

                回答：""")

        self.chain = (
            {"context": self.retriever.as_retriever(), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def invoke(self, question: str) -> Dict[str, Any]:
        """
        调用RAG链回答问题
        
        question: 问题

        returns: 包含答案和上下文的字典
        """
        try:
            # 检索相关文档
            retriever = self.retriever.as_retriever()
            docs = retriever.invoke(question)
            
            if not docs:
                print(f"未找到相关文档: {question}")
                return {
                    "success": False,
                    "answer": "未找到相关信息",
                    "context": "",
                    "source_documents": []
                }
            
            # 提取上下文
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # 生成回答
            answer = self.chain.invoke(question)
            
            return {
                "success": True,
                "answer": answer,
                "context": context,
                "source_documents": docs
            }
            
        except Exception as e:
            print(f"RAG链执行失败: {str(e)}")
            return {
                "success": False,
                "answer": f"处理问题时出错: {str(e)}",
                "context": "",
                "source_documents": []
            }