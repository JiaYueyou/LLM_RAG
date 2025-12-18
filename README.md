# LLM RAG 问答系统

基于 LangChain 1.0 和向量数据库的智能问答系统，支持文档检索增强生成(RAG)和智能代理功能。

## 项目目录

```
LLM_RAG/
├── app/
│   ├── agents/           # 智能代理模块
│   │   └── qa_agent.py   # 问答代理实现
│   ├── data/             # 数据处理模块
│   │   ├── insert_data.py # 数据插入脚本
│   │   └── loader.py     # 文档加载器
│   ├── rag/              # RAG检索增强生成模块
│   │   ├── chain.py      # RAG链实现
│   │   └── retriever.py  # 向量检索器
│   └── tools/            # 工具模块
│       ├── calculator.py # 计算器工具
│       └── search_tool.py # 搜索工具
├── docs/                 # 文档目录
├── .env                  # 环境配置文件
├── config.py             # 应用配置
├── environment.yml       # Conda环境配置文件
└── main.py               # 主程序入口
```

## 项目功能介绍

### 主要功能

1. **文档问答系统**：基于用户上传的文档内容进行智能问答
2. **RAG检索增强**：结合向量检索和大语言模型，提供准确的答案
3. **智能代理**：自动判断问题类型，选择合适的工具或策略
4. **多格式支持**：支持PDF、TXT、DOCX、MD等多种文档格式
5. **交互式界面**：提供命令行交互式问答体验

### 技术栈

- **LangChain 1.0**：大语言模型应用开发框架
- **ChromaDB**：向量数据库，用于文档存储和相似度检索
- **OpenAI API**：提供大语言模型服务
- **Python 3.10+**：开发语言

### 适用场景

- 企业知识库问答系统
- 技术文档智能检索
- 学习资料问答助手
- 专业领域知识咨询

## 操作指南

### 环境配置

1. **克隆项目**
   ```bash
   git clone <项目地址>
   cd LLM_RAG
   ```

2. **创建并激活conda环境**
   ```bash
   conda env create -f environment.yml
   conda activate llm-rag
   ```

3. **配置环境变量**
   
   创建 `.env` 文件并配置以下内容：
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL=gpt-3.5-turbo
   VECTOR_DB_PATH=./data/vector_db
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   ```
   
   注意：确保项目根目录下有 `environment.yml` 文件，用于配置conda环境。如果文件不存在，可以参考以下内容创建：
   ```yaml
   name: llm-rag
   channels:
     - defaults
   dependencies:
     - python=3.10
     - pip
     - pip:
       - langchain
       - langchain-openai
       - langchain-chroma
       - langchain-community
       - chromadb
       - python-dotenv
       - pypdf
       - docx2txt
       - chardet
   ```

### 启动方法

1. **数据准备**
   
   将需要问答的文档放入 `docs` 目录下，然后运行数据插入脚本：
   ```bash
   python app/data/insert_data.py
   ```

2. **启动问答系统**
   
   ```bash
   # 交互模式
   python main.py
   
   # 单次查询模式
   python main.py --query "你的问题"
   ```

### 关键操作流程

1. **文档准备**：将文档放入 `docs` 目录
2. **数据插入**：运行 `insert_data.py` 将文档加载到向量数据库
3. **启动系统**：运行 `main.py` 启动问答系统
4. **交互问答**：在交互界面中输入问题，获取答案

## 可扩展功能清单

1. **多模态文档支持**：扩展支持图片、表格、音频等多模态内容
2. **对话历史管理**：实现持久化对话历史和上下文记忆
3. **多用户支持**：添加用户管理和权限控制
4. **Web界面**：开发基于Web的用户界面
5. **智能文档摘要**：自动生成文档摘要和关键信息提取

## 功能扩展指南

### 1. 多模态文档支持

**实现思路**：
- 扩展文档加载器，支持图片OCR、表格解析
- 集成多模态大模型（如GPT-4V）
- 修改向量存储策略，支持多模态嵌入

**核心模块**：
- `app/data/loader.py`：扩展文档加载功能
- `app/rag/retriever.py`：修改向量存储和检索逻辑

**技术储备**：
- 图像处理库（PIL, OpenCV）
- OCR技术（Tesseract, PaddleOCR）
- 多模态嵌入模型

### 2. 对话历史管理

**实现思路**：
- 设计对话历史数据模型
- 实现对话历史存储和检索机制
- 修改问答代理，整合历史上下文

**核心模块**：
- `app/agents/qa_agent.py`：增强对话上下文处理
- 新增 `app/memory/` 模块：管理对话历史

**技术储备**：
- 数据库知识（SQLite, PostgreSQL）
- 对话状态管理
- 上下文窗口优化技术

### 3. 多用户支持

**实现思路**：
- 设计用户认证和授权系统
- 实现用户数据隔离
- 添加用户管理界面

**核心模块**：
- 新增 `app/auth/` 模块：用户认证
- 新增 `app/users/` 模块：用户管理
- 修改 `main.py`：添加用户认证流程

**技术储备**：
- 用户认证技术（JWT, OAuth）
- 数据库设计
- 权限控制模型

### 4. Web界面

**实现思路**：
- 设计RESTful API接口
- 开发前端界面
- 实现实时通信功能

**核心模块**：
- 新增 `app/api/` 模块：API接口
- 新增 `frontend/` 目录：前端代码

**技术储备**：
- Web框架（FastAPI, Flask）
- 前端框架（React, Vue）
- WebSocket通信

### 5. 智能文档摘要

**实现思路**：
- 实现文档摘要算法
- 集成关键信息提取技术
- 设计摘要展示界面

**核心模块**：
- 新增 `app/summary/` 模块：文档摘要功能
- 修改 `app/rag/chain.py`：集成摘要功能

**技术储备**：
- 文本摘要算法
- 关键词提取技术
- NLP处理库（spaCy, NLTK）