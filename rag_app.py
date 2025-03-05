import os
import sys
import time

def main():
    """RAG知识库应用主入口"""
    print("="*50)
    print("RAG知识库问答系统")
    print("="*50)
    
    # 检查是否有文档
    docs_dir = "docs"
    if not os.path.exists(docs_dir) or len(os.listdir(docs_dir)) == 0:
        print("错误: 没有找到任何文档。请先运行 setup_environment.py")
        return
    
    # 导入RAGAgent
    try:
        from src.agents.rag_agent import RAGAgent
    except ImportError as e:
        print(f"导入RAGAgent失败: {str(e)}")
        print("请先运行 setup_environment.py 设置环境")
        return
    
    # 数据库目录
    db_dir = "vector_db"
    
    # 检查是否需要构建知识库
    if not os.path.exists(db_dir) or len(os.listdir(db_dir) if os.path.isdir(db_dir) else []) == 0:
        print("正在构建知识库...")
        try:
            agent = RAGAgent(
                docs_dir=docs_dir,
                persist_dir=db_dir,
                api_base="填写api接口",
                api_key="填写api密钥"
            )
            print("知识库构建完成!")
        except Exception as e:
            print(f"构建知识库时出错: {str(e)}")
            return
    else:
        try:
            print("正在加载已有知识库...")
            agent = RAGAgent(
                docs_dir=docs_dir,
                persist_dir=db_dir,
                api_base="填写api接口",
                api_key="填写api密钥"
            )
            print("知识库加载完成!")
        except Exception as e:
            print(f"加载知识库时出错: {str(e)}")
            return
    
    # 交互式问答循环
    print("\n您现在可以向知识库提问了。输入'exit'退出。")
    while True:
        try:
            question = input("\n问题: ")
            if question.lower() in ['exit', 'quit', '退出']:
                break
                
            if not question.strip():
                continue
                
            print("正在查询知识库...")
            start_time = time.time()
            response = agent.query(question)
            end_time = time.time()
            
            print(f"\n回答: {response}")
            print(f"查询用时: {end_time - start_time:.2f}秒")
            
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except Exception as e:
            print(f"查询时出错: {str(e)}")
    
if __name__ == "__main__":
    main()
