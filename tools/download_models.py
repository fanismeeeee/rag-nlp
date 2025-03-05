"""
在开启VPN的情况下下载并缓存所需的模型
"""
import os
import sys
import time
from pathlib import Path
import shutil

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def download_and_cache_models():
    """下载并缓存Huggingface模型到本地"""
    print("="*60)
    print("  Huggingface模型下载工具  ")
    print("  请确保您已经开启了VPN或代理  ")
    print("="*60)
    
    # 确认是否已开启VPN
    answer = input("\n请确认您已开启VPN或代理连接? (y/n): ")
    if answer.lower() != 'y':
        print("请先开启VPN或代理连接，然后再运行此脚本。")
        return
    
    # 设置模型存储路径，使用正斜杠避免转义问题
    models_dir = os.path.join(project_root, "models")
    models_dir = models_dir.replace("\\", "/")  # 替换反斜杠为正斜杠
    os.makedirs(models_dir, exist_ok=True)
    
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    local_model_path = os.path.join(models_dir, "all-MiniLM-L6-v2")
    local_model_path = local_model_path.replace("\\", "/")  # 替换反斜杠为正斜杠
    
    print(f"将模型下载到: {local_model_path}")
    
    # 下载嵌入模型
    try:
        print(f"\n开始下载模型: {embedding_model_name}")
        from sentence_transformers import SentenceTransformer
        
        # 先尝试下载模型
        print("正在下载模型，这可能需要几分钟...")
        model = SentenceTransformer(embedding_model_name)
        
        # 保存模型到本地
        print(f"正在保存模型到: {local_model_path}")
        model.save(local_model_path)
        print("✓ 模型下载并保存成功!")
        
        # 打印模型位置信息
        print("\n模型信息:")
        print(f"- 原始模型名称: {embedding_model_name}")
        print(f"- 本地模型路径: {local_model_path}")
        
        print("\n您现在可以关闭VPN，模型已成功下载到本地。")
        print("下一步，请运行 tools/update_with_local_models.py 脚本更新RAGAgent以使用本地模型。")
        
    except Exception as e:
        print(f"下载模型时出错: {str(e)}")
        print("请检查您的网络连接，确保VPN或代理连接正常。")

if __name__ == "__main__":
    download_and_cache_models()
