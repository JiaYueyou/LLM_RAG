# 简单的计算器工具，用于执行基本数学计算

import re

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    """计算器输入模型"""
    expression: str = Field(description="要计算的数学表达式，例如: 2 + 3 * 4")


class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "用于执行基本数学计算的工具"
    args_schema: type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """
        执行计算
        
        expression: 数学表达式
            
        returns: 计算结果
        """
        try:
            # 安全性检查：只允许数字、基本运算符和空格
            if not re.match(r'^[\d\s\.\+\-\*\/\(\)]+$', expression):
                return f"错误：表达式包含不安全字符: {expression}"
            
            # 计算表达式
            result = eval(expression)
            
            return f"计算结果: {result}"
            
        except Exception as e:
            print(f"计算错误: {str(e)}")
            return f"计算错误: {str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """异步执行计算"""
        return self._run(expression)
    
    @property
    def tool(self):
        """返回工具对象，用于代理集成"""
        return self