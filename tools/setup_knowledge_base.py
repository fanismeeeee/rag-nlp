import os
import sys

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def setup_knowledge_base():
    """创建知识库所需的目录结构"""
    print("=== RAG知识库目录结构设置工具 ===")
    
    # 创建文档目录
    docs_dir = os.path.join(project_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    # 创建向量数据库目录
    vector_db_dir = os.path.join(project_root, "vector_db")
    os.makedirs(vector_db_dir, exist_ok=True)
    
    # 创建模型目录
    models_dir = os.path.join(project_root, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    print("\n已创建知识库目录结构:")
    print(f"- 文档目录: {docs_dir}")
    print(f"- 向量数据库: {vector_db_dir}")
    print(f"- 模型目录: {models_dir}")
    
    print("\n下一步:")
    print("1. 将文档放入docs目录")
    print("2. 运行 python tools/download_models.py 下载模型")
    print("3. 运行 python tools/ingest_documents.py 构建知识库")
    print("4. 运行 python rag_app.py 启动问答系统")

if __name__ == "__main__":
    setup_knowledge_base()
