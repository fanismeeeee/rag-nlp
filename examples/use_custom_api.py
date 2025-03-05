import sys
import os

# 将项目根目录添加到Python模块搜索路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 获取项目根目录
sys.path.insert(0, project_root)  # 添加到搜索路径

# 检查并安装必要的依赖
try:
    import sentence_transformers
except ImportError:
    print("正在安装必要的依赖包...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers"])
    print("依赖包安装完成！")

from src.agents.rag_agent import RAGAgent

# 初始化使用第三方API的RAG代理
agent = RAGAgent(
    docs_dir="docs",
    persist_dir="vector_db",  # 修改为不同的目录名，避免与现有文件冲突
    api_base="https://openai.azure.com/v1",
    api_key="sk-<KEY>"
)

# 测试查询
question = "我现在擤鼻涕、浑身无力、腰还疼，是普通感冒吗还是流感？"
response = agent.query(question)
print(f"问题: {question}")
print(f"回答: {response}")
