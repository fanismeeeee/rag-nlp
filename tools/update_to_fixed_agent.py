"""
更新系统使用修复版本的RAG代理
"""
import os
import shutil
import sys

def show_header():
    """显示脚本标题"""
    print("="*60)
    print("  更新到修复版本的RAG代理")
    print("="*60)

def backup_original_agent():
    """备份原始RAG代理文件"""
    src_path = os.path.join("src", "agents", "rag_agent.py")
    backup_path = os.path.join("src", "agents", "rag_agent.py.bak")
    
    if not os.path.exists(src_path):
        print(f"错误: 找不到原始代理文件 {src_path}")
        return False
    
    try:
        shutil.copy2(src_path, backup_path)
        print(f"✓ 已备份原始RAG代理到 {backup_path}")
        return True
    except Exception as e:
        print(f"备份原始RAG代理时出错: {str(e)}")
        return False

def update_agent():
    """用修复版本替换RAG代理"""
    fixed_path = os.path.join("src", "agents", "fixed_rag_agent.py")
    target_path = os.path.join("src", "agents", "rag_agent.py")
    
    if not os.path.exists(fixed_path):
        print(f"错误: 找不到修复版代理文件 {fixed_path}")
        return False
    
    try:
        shutil.copy2(fixed_path, target_path)
        print(f"✓ 已用修复版替换原始RAG代理")
        return True
    except Exception as e:
        print(f"替换RAG代理时出错: {str(e)}")
        return False

def main():
    """主函数"""
    show_header()
    
    print("此脚本将用修复版本替换当前的RAG代理文件。")
    print("原始文件将被备份为 rag_agent.py.bak")
    
    response = input("\n是否继续? [y/N]: ")
    if response.lower() != 'y':
        print("操作已取消")
        return
    
    # 备份原始代理
    if not backup_original_agent():
        print("由于备份失败，操作已中止")
        return
    
    # 更新代理
    if update_agent():
        print("\n✅ RAG代理已成功更新到修复版本！")
        print("现在可以重新启动系统，不再有弃用警告。")
    else:
        print("\n❌ 更新RAG代理失败。")
        print("请手动检查并修复问题。")

if __name__ == "__main__":
    main()
