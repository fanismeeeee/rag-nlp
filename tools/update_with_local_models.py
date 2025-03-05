"""
更新RAGAgent类以使用本地下载的模型
"""
import os
import re
import sys

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def update_agent_with_local_model():
    """修改RAGAgent以使用本地模型"""
    file_path = os.path.join(project_root, "src", "agents", "rag_agent.py")
    
    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        return False
    
    # 本地模型路径 - 使用项目根目录路径
    local_model_path = os.path.join(project_root, "models", "all-MiniLM-L6-v2")
    
    # 将Windows路径中的反斜杠替换为正斜杠，避免转义问题
    local_model_path = local_model_path.replace("\\", "/")
    
    print(f"本地模型路径: {local_model_path}")
    
    if not os.path.exists(local_model_path):
        print(f"错误: 本地模型不存在于 {local_model_path}")
        print("请先运行 tools/download_models.py 脚本下载模型")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 查找任何包含HuggingFaceEmbeddings初始化的行
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "HuggingFaceEmbeddings" in line and "model_name" in line:
                print(f"找到需要替换的行: {line}")
                # 替换整行
                lines[i] = f'        self.embeddings = HuggingFaceEmbeddings(model_name="{local_model_path}")'
                print(f"替换为: {lines[i]}")
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as outfile:
                    outfile.write('\n'.join(lines))
                
                print(f"✓ 成功更新 {file_path}")
                return True
        
        print("未找到需要替换的嵌入模型初始化代码")
        return False
            
    except Exception as e:
        print(f"更新文件时出错: {str(e)}")
        return False

def check_environment():
    """检查环境是否已安装必要的包"""
    try:
        import sentence_transformers
        return True
    except ImportError:
        print("错误: sentence-transformers 包未安装")
        print("请先运行 tools/setup_environment.py 安装必要的依赖")
        return False

if __name__ == "__main__":
    print("更新RAGAgent以使用本地模型...")
    
    if check_environment():
        if update_agent_with_local_model():
            print("\n更新完成! 现在您可以在没有VPN的情况下运行RAG系统。")
            print("\n建议测试运行:")
            print("python rag_app.py")
