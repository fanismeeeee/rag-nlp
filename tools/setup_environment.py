import subprocess
import sys
import os
import time

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def force_install_dependencies():
    """强制安装指定版本的依赖，确保环境一致"""
    # 先卸载可能冲突的包
    uninstall_packages = [
        "numpy",
        "sentence-transformers",
        "chromadb"
    ]
    
    print("1. 卸载可能存在版本冲突的包...")
    for package in uninstall_packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package], 
                          check=False)
        except Exception as e:
            print(f"卸载 {package} 时出错: {str(e)}")
    
    # 安装指定版本的依赖
    install_packages = [
        "numpy==1.24.3",  # 使用稳定的1.x版本
        "sentence-transformers==2.2.2",
        "chromadb==0.4.18",
        "langchain-huggingface",
        "langchain-chroma",
        "pypdf",
        "python-docx"
    ]
    
    print("\n2. 安装指定版本的依赖...")
    for package in install_packages:
        print(f"安装 {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"✗ {package} 安装失败")
    
    print("\n3. 更新RAG代理实现...")
    update_rag_agent()
    
    print("\n4. 创建示例文档...")
    create_sample_txt()
    
    print("\n环境设置完成!")
    print("您现在可以运行 python rag_app.py 来启动RAG知识库应用")

def update_rag_agent():
    """更新RAGAgent类以使用非弃用版本的类"""
    file_path = os.path.join(project_root, "src", "agents", "rag_agent.py")
    
    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 替换导入语句
    changes_made = False
    
    # 替换HuggingFaceEmbeddings导入
    if "from langchain.embeddings import HuggingFaceEmbeddings" in content:
        content = content.replace(
            "from langchain.embeddings import HuggingFaceEmbeddings",
            "from langchain_huggingface import HuggingFaceEmbeddings"
        )
        changes_made = True
    
    # 替换Chroma导入
    if "from langchain.vectorstores import Chroma" in content:
        content = content.replace(
            "from langchain.vectorstores import Chroma",
            "from langchain_chroma import Chroma"
        )
        changes_made = True
    
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"已成功更新 {file_path} 中的导入语句")
    else:
        print(f"未在 {file_path} 中找到需要更新的导入语句")

def create_sample_txt():
    """创建一个示例文本文档"""
    docs_dir = os.path.join(project_root, "docs")
    
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    sample_file = os.path.join(docs_dir, "sample.txt")
    
    content = """# RAG知识库系统

## 简介
RAG (Retrieval Augmented Generation) 是一种结合了检索和生成功能的AI模型架构。
它通过从知识库中检索相关信息来增强大语言模型的回答质量和准确性。

## 主要特点
1. 信息准确性高：回答基于检索到的最新知识
2. 可以处理专业领域问题：通过导入专业文档提升特定领域回答质量
3. 可减少大语言模型的"幻觉"：回答有事实依据

## 应用场景
- 企业内部知识问答系统
- 技术文档智能助手
- 客户支持自动化
- 教育培训辅助工具

这是一个测试文档，用来验证RAG系统的文档处理和问答功能是否正常工作。
"""
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"示例文档已创建: {sample_file}")

if __name__ == "__main__":
    print("RAG知识库系统 - 环境设置工具")
    print("="*50)
    force_install_dependencies()
