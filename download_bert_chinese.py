"""
下载bert-base-chinese模型
"""
import os
import shutil
from transformers import BertModel, BertTokenizer

def download_model():
    print("开始下载bert-base-chinese模型...")
    
    # 创建模型目录
    model_dir = os.path.join("models", "bert-base-chinese")
    os.makedirs(model_dir, exist_ok=True)
    
    try:
        # 下载模型和分词器
        print("下载模型文件...")
        model = BertModel.from_pretrained("bert-base-chinese")
        tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        
        # 保存模型和分词器
        print(f"保存模型到 {model_dir}")
        model.save_pretrained(model_dir)
        tokenizer.save_pretrained(model_dir)
        
        print("模型下载完成！")
        print(f"模型保存在: {os.path.abspath(model_dir)}")
        
        # 列出下载的文件
        print("\n下载的文件:")
        for file in os.listdir(model_dir):
            file_path = os.path.join(model_dir, file)
            file_size = os.path.getsize(file_path)
            print(f" - {file} ({file_size/1024/1024:.2f} MB)")
            
        return True
    except Exception as e:
        print(f"下载模型时出错: {str(e)}")
        return False

if __name__ == "__main__":
    download_model() 