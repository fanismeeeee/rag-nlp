# RAG知识库问答系统

## 项目概述

RAG知识库问答系统是一个基于检索增强生成（Retrieval-Augmented Generation, RAG）技术的智能问答平台。该系统允许用户导入自己的文档，构建知识库，然后通过自然语言提问获取精准的答案。系统会从导入的文档中检索相关信息，结合大语言模型的能力，生成基于事实和上下文的回答。

**核心特点**:
- 💾 支持多种文档格式导入
- 🔍 基于语义向量检索相关文档片段
- 🤖 利用大语言模型生成准确回答
- 🖥️ 提供命令行和图形用户界面
- 🧩 支持多种嵌入模型
- 🌐 优化的中文处理能力
- 💭 对话记忆功能
- 📚 文档来源追踪

## 技术架构

### 核心组件

1. **RAG代理 (RAGAgent)**: 系统的核心类，负责处理文档嵌入、检索和问答生成
2. **文档处理**: 支持PDF、Word和文本文件的导入和处理
3. **向量嵌入**: 支持多种HuggingFace模型，包括中文优化模型
4. **向量存储**: 使用Chroma数据库高效存储和检索文档向量
5. **大语言模型集成**: 通过API连接大语言模型生成回答
6. **用户界面**: 提供现代化的命令行和图形用户界面

### 技术栈

- **Python 3.8+**: 主要开发语言
- **LangChain**: RAG工作流框架
- **HuggingFace Transformers**: 文本嵌入模型
- **Chroma DB**: 向量数据库
- **PySide6**: 现代化图形用户界面
- **OpenAI API**: LLM访问

## 项目结构

```
/d:/code/python/rag-knowledge-base/
├── manage_rag.py              # 主管理界面
├── rag_app.py                 # 命令行应用入口
├── simple_gui_tk.py           # Tk图形界面
├── start_gui.py               # 安全启动器（解决兼容性问题）
├── docs/                      # 存放导入的文档
├── models/                    # 存放嵌入模型
│   └── all-MiniLM-L6-v2/      # 默认嵌入模型
├── vector_db/                 # 向量数据库存储位置
├── src/
│   ├── agents/
│   │   ├── rag_agent.py       # RAG代理实现
│   │   └── rag_agent_fixed.py # 修复版RAG代理
│   ├── utils/
│   │   ├── document_loaders.py # 文档加载工具
│   │   └── numpy_patch.py      # NumPy兼容性补丁
│   └── prompts/
│       └── rag_prompts.py     # 系统提示模板
└── tools/
    ├── setup_environment.py   # 环境设置工具
    ├── setup_knowledge_base.py # 创建知识库结构
    ├── download_models.py     # 下载嵌入模型
    ├── ingest_documents.py    # 导入文档工具
    ├── update_with_local_models.py # 配置使用本地模型
    ├── fix_compatibility.py   # 兼容性问题修复
    ├── fix_numpy_compatibility.py # NumPy兼容性修复
    └── use_fixed_agent.py     # 应用修复版RAG代理
```

## 安装与设置

### 系统要求

- Python 3.8+
- 约2GB磁盘空间 (主要用于存储嵌入模型)
- 4GB+ RAM
- 互联网连接 (用于初始下载模型和API访问)

### 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/ViolentAyang/rag-knowledge-base.git
   cd rag-knowledge-base
   ```

2. **使用管理工具设置环境**
   ```bash
   python manage_rag.py
   ```
   选择选项1"设置环境（安装依赖包）"

3. **创建知识库结构**
   在管理工具中选择选项2"创建知识库目录结构"

4. **下载嵌入模型**
   在管理工具中选择选项3"下载模型"
   
   *注意: 需要VPN访问HuggingFace*

5. **放置文档**
   将您的PDF或文本文档放入`docs`目录

6. **导入文档到知识库**
   在管理工具中选择选项4"导入文档到知识库"

## 使用指南

### 管理界面

运行主管理界面：
```bash
python manage_rag.py
```

管理界面提供以下选项：
- 环境设置
- 知识库管理
- 模型下载
- 文档导入
- 启动问答系统
- 问题修复工具

### 命令行界面

启动命令行问答系统：
```bash
python rag_app.py
```
或从管理界面选择选项6。

使用方法：
1. 启动后系统将加载知识库
2. 在提示符后输入您的问题
3. 系统会从知识库中检索相关信息并生成回答
4. 输入`exit`退出系统

### 图形用户界面

启动图形界面：
```bash
python simple_gui_tk.py
```
或从管理界面选择选项7。

如果遇到兼容性问题，可以使用安全启动器：
```bash
python start_gui.py
```
或从管理界面选择选项10。

GUI界面功能：
1. 点击"初始化知识库"按钮加载知识库
2. 在问题输入框中输入问题
3. 点击"发送问题"或按Ctrl+Enter提交
4. 系统会在对话区域显示问题和回答
5. 右下角会显示查询用时
6. "清空对话"按钮可清除当前对话历史

## 自定义与扩展

### 添加新的文档格式支持

1. 修改`src/utils/document_loaders.py`文件
2. 添加新的文件格式处理逻辑

### 使用不同的嵌入模型

1. 下载所需的HuggingFace模型
2. 修改`src/agents/rag_agent.py`中的模型路径

### 配置不同的API端点

1. 修改RAGAgent初始化参数中的api_base和api_key
2. 或在环境变量中设置相应的API配置

### 添加记忆功能

当前系统不保留对话历史。要添加记忆功能：

1. 在RAGAgent中初始化ConversationBufferMemory
2. 将memory传递给ConversationalRetrievalChain
3. 修改query方法以维护对话历史

## 疑难解答

### NumPy 2.0兼容性问题

如果您使用NumPy 2.0版本，可能会遇到与chromadb不兼容的问题。解决方法：

1. 从管理界面选择选项9"修复NumPy兼容性问题"
2. 选择推荐的解决方案（通常是降级NumPy到1.25.2版本）
3. 重新启动程序

### LangChain导入错误

如果出现类似于以下的错误：
```
cannot import name 'ConversationBufferMemory' from 'langchain_community.memory'
```

解决方法：
1. 从管理界面选择选项8"修复所有警告和错误"
2. 或选择选项11"使用全新修复版RAG代理"
3. 重新启动程序

### 查询方法错误

如果出现类似于以下的错误：
```
Missing some input keys: {'chat_history'}
```

解决方法：
1. 从管理界面选择选项11"使用全新修复版RAG代理"
2. 或手动修改`src/agents/rag_agent.py`文件中的query方法，确保包含chat_history参数

## 技术细节

### 文档处理流程

1. 加载文档 (PDF/TXT)
2. 文本分割 (递归字符分割器)
3. 文本嵌入 (HuggingFace模型)
4. 向量存储 (Chroma DB)

### RAG工作流程

1. 用户提问
2. 问题嵌入向量化
3. 向量相似度检索
4. 构建提示上下文
5. LLM生成回答
6. 返回结果给用户

### 使用的模型

- **嵌入模型**: 默认使用all-MiniLM-L6-v2
- **LLM**: 通过API访问，兼容OpenAI接口

## 功能更新（2024年6月）

### 1. 检索召回数量提升
- 支持自定义初步检索召回数量（top_k），提升相关文档覆盖率。

### 2. 交叉编码器重排序
- 集成了 Cross-Encoder（如 cross-encoder/ms-marco-MiniLM-L-6-v2），对初步召回的文档与问题进行逐对重排序，显著提升相关性排序精度。

### 3. query_with_sources 支持参数
- `query_with_sources(question, top_k=15, top_n=8)` 可灵活调整召回和最终返回文档数量。

### 4. 自动化API Key注入
- 支持通过环境变量自动注入 OpenAI API Key，无需手动输入，提升易用性。

## 结语

RAG知识库问答系统提供了一个强大且灵活的框架，帮助您利用自己的文档构建智能问答系统。系统的模块化设计使其易于扩展和自定义，可以根据特定需求进行调整。

无论是个人知识管理、企业文档检索还是专业领域问答，本系统都能提供有价值的解决方案。

---

*本项目基于MIT许可证开源*