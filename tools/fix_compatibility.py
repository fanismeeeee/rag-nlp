"""
修复兼容性问题的工具脚本
解决NumPy 2.0和LangChain弃用类的问题
"""

import os
import subprocess
import sys
import pkg_resources

def show_header():
    """显示脚本标题"""
    print("="*60)
    print("  依赖兼容性问题修复工具")
    print("="*60)

def check_numpy_version():
    """检查并修复NumPy版本问题"""
    try:
        import numpy as np
        numpy_version = np.__version__
        print(f"当前NumPy版本: {numpy_version}")
        
        if numpy_version.startswith("2."):
            print("检测到NumPy 2.x，这可能导致与某些依赖库不兼容")
            
            response = input("是否降级NumPy到1.25.2版本? [y/N]: ")
            if response.lower() == "y":
                print("正在降级NumPy...")
                subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.25.2", "--force-reinstall"], check=True)
                print("NumPy已降级到1.25.2")
                print("请重新启动程序以应用更改")
                return True
            else:
                print("跳过NumPy降级")
    except ImportError:
        print("未安装NumPy")
    
    return False

def install_langchain_packages():
    """安装最新的LangChain相关包"""
    print("\n正在安装/更新LangChain兼容包...")
    packages = [
        "langchain-community",
        "langchain-huggingface",
        "langchain-chroma"
    ]
    
    for package in packages:
        print(f"安装/更新 {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", package], check=True)
    
    print("LangChain相关包更新完成")

def fix_rag_agent_code():
    """修复RAG代理中的代码问题"""
    rag_agent_path = os.path.join("src", "agents", "rag_agent.py")
    
    if not os.path.exists(rag_agent_path):
        print(f"错误: 找不到文件 {rag_agent_path}")
        return
    
    with open(rag_agent_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 修复导入语句
    modified_content = content
    
    # 修复HuggingFaceEmbeddings导入
    if "from langchain_community.embeddings import HuggingFaceEmbeddings" in content:
        modified_content = modified_content.replace(
            "from langchain_community.embeddings import HuggingFaceEmbeddings",
            "from langchain_huggingface import HuggingFaceEmbeddings"
        )
    
    # 修复Chroma导入
    if "from langchain_community.vectorstores import Chroma" in content:
        modified_content = modified_content.replace(
            "from langchain_community.vectorstores import Chroma",
            "from langchain_chroma import Chroma"
        )
    
    # 修复np.float_问题（如果存在）
    if "np.float_" in modified_content:
        modified_content = modified_content.replace("np.float_", "np.float64")
    
    # 如果内容发生了变化，才写回文件
    if content != modified_content:
        with open(rag_agent_path, "w", encoding="utf-8") as f:
            f.write(modified_content)
        print(f"✓ 已更新 {rag_agent_path} 中的导入语句和类型")
    else:
        print(f"未发现需要修复的问题在 {rag_agent_path}")

def main():
    """主函数"""
    show_header()
    
    numpy_changed = check_numpy_version()
    if numpy_changed:
        print("已降级NumPy，请重启程序以避免导入错误")
        return
    
    install_langchain_packages()
    fix_rag_agent_code()
    
    print("\n兼容性问题修复完成！现在可以尝试重新运行RAG应用了。")

if __name__ == "__main__":
    main()
