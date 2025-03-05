"""
使用全新修复版RAG代理替换现有代理
"""
import os
import sys
import shutil

def show_header():
    """显示脚本标题"""
    print("="*60)
    print("  应用全新修复版RAG代理")
    print("="*60)

def backup_original_agent():
    """备份原始RAG代理文件"""
    src_path = os.path.join("src", "agents", "rag_agent.py")
    backup_path = os.path.join("src", "agents", "rag_agent_backup.py")
    
    if not os.path.exists(src_path):
        print(f"错误: 找不到源文件 {src_path}")
        return False
    
    try:
        shutil.copy2(src_path, backup_path)
        print(f"✓ 已备份原始RAG代理到 {backup_path}")
        return True
    except Exception as e:
        print(f"备份原始文件时出错: {str(e)}")
        return False

def replace_with_fixed_agent():
    """用修复版RAG代理替换现有文件"""
    fixed_path = os.path.join("src", "agents", "rag_agent_fixed.py")
    target_path = os.path.join("src", "agents", "rag_agent.py")
    
    if not os.path.exists(fixed_path):
        print(f"错误: 找不到修复版文件 {fixed_path}")
        return False
    
    try:
        shutil.copy2(fixed_path, target_path)
        print(f"✓ 已用全新修复版代替现有RAG代理")
        return True
    except Exception as e:
        print(f"替换文件时出错: {str(e)}")
        return False

def main():
    """主函数"""
    show_header()
    
    print("此脚本将用全新修复版RAG代理替换现有文件。")
    print("原始文件将被备份为 rag_agent_backup.py")
    
    response = input("\n是否继续? [y/N]: ")
    if response.lower() != 'y':
        print("操作已取消")
        return
    
    if not backup_original_agent():
        print("由于备份失败，操作已中止")
        return
    
    if replace_with_fixed_agent():
        print("\n✅ RAG代理已成功替换为全新修复版！")
        print("现在可以尝试重新运行系统了。")
    else:
        print("\n❌ 替换RAG代理失败！")

if __name__ == "__main__":
    main()
