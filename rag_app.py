import os
import sys
import time
import argparse

def main():
    """RAG知识库应用主入口"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="RAG知识库问答系统 - 支持多种嵌入模型")
    parser.add_argument("--model", type=str, default="distiluse-base-multilingual-cased-v1",
                        help="嵌入模型名称 (默认: distiluse-base-multilingual-cased-v1)")
    parser.add_argument("--docs", type=str, default="docs",
                        help="文档目录 (默认: docs)")
    parser.add_argument("--db", type=str, default="vector_db",
                        help="向量数据库目录 (默认: vector_db)")
    parser.add_argument("--rebuild", action="store_true",
                        help="强制重建知识库")
    args = parser.parse_args()
    
    print("="*50)
    print("RAG知识库问答系统 - 中文优化版")
    print("="*50)
    print(f"使用模型: {args.model}")
    print(f"文档目录: {args.docs}")
    print(f"数据库目录: {args.db}")
    print("="*50)
    
    # 检查是否有文档
    docs_dir = args.docs
    if not os.path.exists(docs_dir) or len(os.listdir(docs_dir)) == 0:
        print("错误: 没有找到任何文档。请先将文档放入docs目录")
        return
    
    # 导入RAGAgent
    try:
        from src.agents.rag_agent import RAGAgent
    except ImportError as e:
        print(f"导入RAGAgent失败: {str(e)}")
        print("请确保已安装所有依赖")
        return
    
    # 检查OpenAI API Key
    if not os.getenv("OPENAI_API_KEY"):
        api_key = input("请输入您的OpenAI API Key: ")
        if api_key.strip():
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            print("错误: 未提供API Key，无法继续")
            return
    
    # 数据库目录
    db_dir = args.db
    
    # 检查是否需要构建知识库
    if args.rebuild or not os.path.exists(db_dir) or len(os.listdir(db_dir) if os.path.isdir(db_dir) else []) == 0:
        print("正在构建知识库...")
        try:
            agent = RAGAgent(
                docs_dir=docs_dir,
                persist_dir=db_dir,
                model_name=args.model
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
                model_name=args.model
            )
            print("知识库加载完成!")
        except Exception as e:
            print(f"加载知识库时出错: {str(e)}")
            return
    
    # 交互式问答循环
    print("\n您现在可以向知识库提问了。输入'exit'退出，输入'clear'清除对话历史。")
    while True:
        try:
            question = input("\n问题: ")
            if question.lower() in ['exit', 'quit', '退出']:
                break
                
            if question.lower() in ['clear', '清除', '清空']:
                agent.clear_memory()
                print("对话历史已清除")
                continue
                
            if not question.strip():
                continue
                
            print("正在查询知识库...")
            start_time = time.time()
            response = agent.query(question)
            end_time = time.time()
            
            print(f"\n回答: {response['answer']}")
            
            # 显示来源文档
            sources = response.get("source_documents", [])
            if sources:
                print("\n信息来源:")
                for i, doc in enumerate(sources[:3], 1):
                    source = doc.metadata.get("source", "未知来源")
                    print(f"{i}. {os.path.basename(source)}")
            
            print(f"查询用时: {end_time - start_time:.2f}秒")
            
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except Exception as e:
            print(f"查询时出错: {str(e)}")
    
if __name__ == "__main__":
    main()
