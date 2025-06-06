import os
import sys
import shutil

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.agents.rag_agent import RAGAgent

def main():
    print("=== RAG知识库文档导入工具 ===")
    
    # 检查docs目录是否有文件
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print(f"已创建{docs_dir}目录，请将文档放入该目录")
        return
    
    # 检查文件数量
    pdf_files = [f for f in os.listdir(docs_dir) if f.endswith('.pdf')]
    docx_files = [f for f in os.listdir(docs_dir) if f.endswith('.docx') or f.endswith('.doc')]
    txt_files = [f for f in os.listdir(docs_dir) if f.endswith('.txt')]
    
    total_files = len(pdf_files) + len(docx_files) + len(txt_files)
    
    if total_files == 0:
        print(f"错误: {docs_dir}目录中没有找到任何支持的文档(PDF/DOCX/TXT)")
        print("请添加文档后再运行此脚本")
        return
    
    print(f"发现以下文档:")
    print(f"- PDF文件: {len(pdf_files)}个")
    print(f"- Word文件: {len(docx_files)}个")
    print(f"- 文本文件: {len(txt_files)}个")
    
    # 确认是否重新创建知识库
    response = input("是否重新构建知识库？这将删除现有的向量数据库 (y/n): ")
    
    if response.lower() == 'y':
        # 使用与use_custom_api.py一致的数据库目录名
        db_dir = "vector_db"
        
        # 安全删除现有向量库
        if os.path.exists(db_dir):
            if os.path.isdir(db_dir):
                shutil.rmtree(db_dir)
                print(f"已删除旧的知识库目录: {db_dir}")
            else:
                # 如果是文件而不是目录，则删除文件
                os.remove(db_dir)
                print(f"已删除旧的知识库文件: {db_dir}")
        
        # 检查是否存在旧的db文件或目录并处理
        old_db = "db"
        if os.path.exists(old_db):
            if os.path.isdir(old_db):
                shutil.rmtree(old_db)
                print(f"已删除旧的知识库目录: {old_db}")
            else:
                os.remove(old_db)
                print(f"已删除旧的知识库文件: {old_db}")
        
        # 创建RAG代理并处理文档
        print("开始构建新知识库...")
        agent = RAGAgent(docs_dir=docs_dir, persist_dir=db_dir,api_base="https://api.ai-gaochao.cn/v1",api_key="sk-LJnOebUUtdz3fZ5V2a3eD48a810c41BfBe7000183bCa0cCf")
        print("知识库构建完成!")
    
    print("\n使用方法:")
    print("from src.agents.rag_agent import RAGAgent")
    print(f"agent = RAGAgent(docs_dir='{docs_dir}', persist_dir='{db_dir}')")
    print("response = agent.query('您的问题')")

if __name__ == "__main__":
    main()
