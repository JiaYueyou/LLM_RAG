# 知识问答 Agent

from typing import Dict, List, Any, Optional
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from config import Config
from app.rag.chain import RAGChain
from app.tools.calculator import CalculatorTool

class QAAgent:
    def __init__(self, use_rag: bool = True):
        """ use_rag: 是否使用RAG功能 """
        self.use_rag = use_rag
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
        
        # 初始化工具
        self.calculator = CalculatorTool()
        self.tools = [self.calculator.tool,]
        
        # 初始化RAG链
        if use_rag:
            self.rag_chain = RAGChain()
        
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """ 创建代理 """
        # 定义系统提示
        system_prompt = """你是一个知识问答助手，能够回答问题、调用工具和执行任务。
            你有以下工具可以使用：
            {tools}

            使用以下格式：
            Question: 你需要回答的问题
            Thought: 你应该思考要做什么
            Action: 选择一个工具
            Action Input: 工具的输入
            Observation: 工具执行的结果
            ... (这个思考/行动/观察可以重复多次)
            Thought: 我现在知道最终答案了
            Final Answer: 对原始问题的最终答案

            请用中文回答问题。"""
        
        agent = create_agent(
            model=f'{Config.MODEL_NAME}',
            tools=self.tools,
            system_prompt=system_prompt
        )
        
        return agent
    
    def invoke(self, question: str, chat_history: Optional[List[tuple]] = None) -> Dict[str, Any]:
        """
        question: 问题
        chat_history: 聊天历史，格式为[(role, message), ...]   
        returns: 包含答案和元数据的字典
        """
        try:
            # 准备聊天历史
            formatted_history = []
            if chat_history:
                for role, message in chat_history:
                    if role == "user":
                        formatted_history.append(HumanMessage(content=message))
                    elif role == "assistant":
                        formatted_history.append(AIMessage(content=message))
            
            # 如果使用RAG，先检索相关文档
            context = ""
            if self.use_rag:
                try:
                    rag_result = self.rag_chain.invoke(question)
                    if rag_result['success']:
                        context = rag_result['context']
                        print(f"检索到相关上下文: {context[:100]}...")
                except Exception as e:
                    print(f"RAG检索失败: {str(e)}")
            
            # 如果有上下文，修改问题
            if context:
                enhanced_question = f"""基于以下上下文回答问题：
                    上下文：
                    {context}

                    问题：{question}"""
            else:
                enhanced_question = question
            
            # 准备输入
            agent_input = {
                "messages": formatted_history + [HumanMessage(content=enhanced_question)]
            }
            
            result = self.agent.invoke(agent_input)
            
            # 提取回答
            answer = ""
            if isinstance(result, dict) and "messages" in result:
                # 从消息中提取最后一条AI消息
                for message in reversed(result["messages"]):
                    if isinstance(message, AIMessage):
                        answer = message.content
                        break
            elif isinstance(result, str):
                answer = result
            elif hasattr(result, "content"):
                answer = result.content
            else:
                answer = str(result)
            
            return {
                "success": True,
                "answer": answer,
                "context": context,
                "intermediate_steps": []
            }
            
        except Exception as e:
            print(f"代理执行失败: {str(e)}")
            return {
                "success": False,
                "answer": f"处理问题出错: {str(e)}",
                "context": "",
                "intermediate_steps": []
            }