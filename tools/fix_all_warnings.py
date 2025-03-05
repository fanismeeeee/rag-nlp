import os
import subprocess
import sys
import re

def show_header():
    """显示脚本标题"""
    print("="*60)
    print("  RAG系统全面修复工具")
    print("="*60)

def install_required_packages():
    """安装必要的包"""
    packages = [
        "langchain-huggingface",
        "langchain-chroma",
        "langchain-openai",
        "langchain-community",
        "langchain"
    ]
    
    print("\n正在安装/更新必要的依赖包...")
    for package in packages:
        print(f"安装/更新 {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-U", package], check=True)
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"✗ {package} 安装失败: {e}")
    
    print("依赖包安装/更新完成")

def fix_rag_agent():
    """修复RAG代理中的所有问题"""
    rag_agent_path = os.path.join("src", "agents", "rag_agent.py")
    
    if not os.path.exists(rag_agent_path):
        print(f"错误: 找不到文件 {rag_agent_path}")
        return False
        
    try:
        with open(rag_agent_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. 修复导入语句
        modified_content = content
        
        # 修复 HuggingFaceEmbeddings 导入
        modified_content = re.sub(
            r"from langchain_community\.embeddings import HuggingFaceEmbeddings",
            "from langchain_huggingface import HuggingFaceEmbeddings",
            modified_content
        )
        
        # 修复 Chroma 导入
        modified_content = re.sub(
            r"from langchain_community\.vectorstores import Chroma",
            "from langchain_chroma import Chroma",
            modified_content
        )
        
        # 2. 修复 __call__ 弃用警告 - 将 qa_chain({"question": question}) 改为 qa_chain.invoke({"question": question})
        modified_content = re.sub(
            r"self\.qa_chain\(\{\"question\": question\}\)",
            "self.qa_chain.invoke({\"question\": question})",
            modified_content
        )
        
        # 3. 修复 query_with_sources 方法中的错误
        # 修正 vector_db 为 vector_store
        modified_content = re.sub(
            r"self\.vector_db\.similarity_search_by_vector",
            "self.vector_store.similarity_search_by_vector",
            modified_content
        )
        
        # 添加 get_completion 方法
        if "def get_completion(self, prompt):" not in modified_content:
            # 找到类的结尾位置（可能是文件结尾或下一个类的开始）
            class_end = modified_content.rfind("def")
            if class_end != -1:
                # 在最后一个方法之后插入新方法
                get_completion_method = """
    def get_completion(self, prompt):
        '''使用LLM获取对提示的响应'''
        return self.llm.predict(prompt)
"""
                # 在最后一个方法的结束位置插入
                lines = modified_content.splitlines()
                inserted = False
                
                for i in range(len(lines)-1, 0, -1):
                    if lines[i].strip().startswith("def ") and "self" in lines[i]:
                        # 找到最后一个方法的结束位置
                        indent_level = 0
                        for j in range(i+1, len(lines)):
                            if lines[j].strip() and not lines[j].startswith(" " * (indent_level+1)):
                                lines.insert(j, get_completion_method.strip())
                                inserted = True
                                break
                        if inserted:
                            break
                                
                if not inserted:  # 如果没有找到合适的位置，添加到文件末尾
                    lines.append(get_completion_method.strip())
                    
                modified_content = "\n".join(lines)
        
        # 将修改后的内容写回文件
        with open(rag_agent_path, "w", encoding="utf-8") as f:
            f.write(modified_content)
            
        print(f"✓ 已更新 {rag_agent_path} 中的代码")
        return True
        
    except Exception as e:
        print(f"修复 {rag_agent_path} 时出错: {str(e)}")
        return False

def main():
    """主函数"""
    show_header()
    
    print("开始全面修复RAG系统中的警告和错误...")
    
    # 安装必要的包
    install_required_packages()
    
    # 修复RAG代理
    success = fix_rag_agent()
    
    if success:
        print("\n✅ 全面修复完成！现在可以尝试重新运行系统了。")
        print("注意: 如果仍有警告，你可以忽略它们，因为这些警告不会影响系统的功能。")
    else:
        print("\n❌ 修复过程中出现错误。请检查日志并尝试手动修复问题。")

if __name__ == "__main__":
    main()