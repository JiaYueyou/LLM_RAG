"""
主程序入口
专注于提供交互式问答功能，不包含文档加载功能
"""

import os
import argparse

from config import Config
from app.rag.retriever import VectorRetriever
from app.agents.qa_agent import QAAgent

class QASystem:
    """问答系统主类 - 专注于问答功能"""
    
    def __init__(self):
        """初始化问答系统"""
        self.retriever = VectorRetriever()
        self.agent = QAAgent(use_rag=True)
        self.chat_history = []
        
        # 检查向量数据库是否存在
        self._check_database_status()
    
    def _check_database_status(self):
        """检查向量数据库状态"""
        db_path = Config.VECTOR_DB_PATH
        db_exists = os.path.exists(os.path.join(db_path, "chroma.sqlite3"))
        
        if not db_exists:
            print("\n向量数据库不存在!")
            print(f"请先执行 'app/insert_data.py' 来加载数据")
            print(f"数据库路径: {db_path}")
    
    def interactive_mode(self):
        """交互式问答模式"""
        print("\n=== 问答系统交互模式 ===")
        print("输入 'quit' 或 'exit' 退出")
        print("输入 'history' 查看聊天历史")
        print("输入 'clear' 清空聊天历史")
        print("输入 'status' 查看数据库状态")
        print("========================\n")
        
        while True:
            try:
                user_input = input("您的问题: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("再见!")
                    break
                
                if user_input.lower() == 'history':
                    self._show_history()
                    continue
                
                if user_input.lower() == 'clear':
                    self.chat_history = []
                    print("聊天历史已清空")
                    continue
                
                if user_input.lower() == 'status':
                    self._show_database_status()
                    continue
                
                # 处理问题
                print("\n思考中...")
                result = self.agent.invoke(user_input, self.chat_history)
                
                if result['success']:
                    answer = result['answer']
                    print(f"\n回答: {answer}")
                    
                    # 更新聊天历史
                    self.chat_history.append(("user", user_input))
                    self.chat_history.append(("assistant", answer))
                    
                    # 显示中间步骤（如果有）
                    if Config.DEBUG and result.get('intermediate_steps'):
                        print("\n[调试信息] 中间步骤:")
                        for step in result['intermediate_steps']:
                            print(f"  - {step}")
                else:
                    print(f"错误: {result['answer']}")
                
                print("\n" + "-" * 50 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n再见!")
                break
            except Exception as e:
                print(f"\n发生错误: {str(e)}")
    
    def _show_history(self):
        """显示聊天历史"""
        if not self.chat_history:
            print("暂无聊天历史")
            return
        
        print("\n======= 聊天历史 =======")
        for i, (role, message) in enumerate(self.chat_history):
            role_name = "用户" if role == "user" else "助手"
            print(f"{i+1}. [{role_name}]: {message}")
        print("=========================\n")
    
    def _show_database_status(self):
        """显示数据库状态"""
        db_path = Config.VECTOR_DB_PATH
        db_exists = os.path.exists(os.path.join(db_path, "chroma.sqlite3"))
        
        print("\n======= 数据库状态 =======")
        print(f"数据库路径: {db_path}")
        print(f"状态: {'已初始化' if db_exists else '未初始化'}")
        
        if db_exists:
            try:
                # 尝试获取基本统计信息
                retriever = self.retriever.as_retriever()
                if retriever:
                    print("向量检索器: 可用")
                else:
                    print("向量检索器: 不可用")
            except Exception as e:
                print(f"获取详细信息时出错: {str(e)}")
        
        print("=========================\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="基于RAG的LangChain问答系统")
    parser.add_argument("--query", type=str, help="单次查询模式")
    
    args = parser.parse_args()
    
    # 创建问答系统
    qa_system = QASystem()
    
    # 单次查询模式
    if args.query:
        result = qa_system.agent.invoke(args.query)
        if result['success']:
            print(result['answer'])
        else:
            print(f"错误: {result['answer']}")
        return
    
    # 交互模式
    qa_system.interactive_mode()


if __name__ == "__main__":
    main()