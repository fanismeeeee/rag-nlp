"""
修复NumPy 2.0与chromadb不兼容的问题
"""
import os
import sys
import subprocess
import importlib

def show_header():
    """显示脚本标题"""
    print("="*60)
    print("  NumPy 2.0兼容性修复工具")
    print("="*60)

def check_numpy_version():
    """检查NumPy版本"""
    try:
        import numpy as np
        numpy_version = np.__version__
        print(f"当前NumPy版本: {numpy_version}")
        
        if numpy_version.startswith("2."):
            return True, numpy_version
        else:
            print("当前NumPy版本低于2.0，不需要修复")
            return False, numpy_version
    except ImportError:
        print("未安装NumPy")
        return False, None

def apply_monkey_patch():
    """应用猴子补丁修复NumPy 2.0兼容性问题"""
    print("\n正在应用NumPy兼容性补丁...")
    
    # 创建补丁代码
    patch_code = """
# NumPy 2.0兼容性补丁
# 修复移除的np.float_类型
import numpy as np
import warnings

if not hasattr(np, 'float_'):
    # 创建别名以兼容旧代码
    np.float_ = np.float64
    warnings.warn("已应用NumPy 2.0兼容性补丁: np.float_ -> np.float64")
"""
    
    # 保存补丁文件
    patch_file = os.path.join("src", "utils", "numpy_patch.py")
    os.makedirs(os.path.dirname(patch_file), exist_ok=True)
    
    with open(patch_file, "w") as f:
        f.write(patch_code)
    
    print(f"✓ 已创建NumPy兼容性补丁: {patch_file}")
    
    # 创建自动加载补丁的启动器脚本
    launcher_code = """
#!/usr/bin/env python
\"\"\"
RAG知识库系统启动器 - 应用NumPy兼容性补丁后启动GUI
\"\"\"
import os
import sys
import importlib.util

# 首先应用NumPy兼容性补丁
patch_path = os.path.join("src", "utils", "numpy_patch.py")
if os.path.exists(patch_path):
    spec = importlib.util.spec_from_file_location("numpy_patch", patch_path)
    numpy_patch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numpy_patch)

# 然后导入并运行GUI
import simple_gui_tk
simple_gui_tk.main()
"""
    
    # 保存启动器脚本
    launcher_file = "start_gui.py"
    with open(launcher_file, "w") as f:
        f.write(launcher_code)
    
    print(f"✓ 已创建启动器脚本: {launcher_file}")
    
    return True

def downgrade_numpy():
    """降级NumPy到兼容版本"""
    print("\n将NumPy降级到1.25.2版本...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.25.2", "--force-reinstall"], check=True)
        print("✓ NumPy已成功降级到1.25.2")
        
        # 尝试导入确认版本
        importlib.reload(__import__("numpy"))
        import numpy as np
        print(f"确认当前NumPy版本: {np.__version__}")
        return True
    except Exception as e:
        print(f"降级NumPy时出错: {str(e)}")
        return False

def fix_chromadb():
    """尝试更新chromadb到最新版本"""
    print("\n正在尝试更新chromadb到最新版本...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "chromadb"], check=True)
        print("✓ chromadb已更新到最新版本")
        return True
    except Exception as e:
        print(f"更新chromadb时出错: {str(e)}")
        return False

def main():
    """主函数"""
    show_header()
    
    is_numpy2, numpy_version = check_numpy_version()
    if not is_numpy2:
        print("不需要修复NumPy兼容性问题")
        return
    
    print("\nNumPy 2.0与某些依赖库不兼容，有以下解决方案：")
    print("1. 降级NumPy到1.25.2版本（推荐，彻底解决兼容性问题）")
    print("2. 应用兼容性补丁并使用专用启动器（临时解决方案）")
    print("3. 尝试更新chromadb到最新版本（可能不会解决问题）")
    
    choice = input("\n请选择解决方案 [1/2/3]: ")
    
    if choice == "1":
        if downgrade_numpy():
            print("\n✅ NumPy已降级，兼容性问题已解决！")
            print("请重新运行程序以应用更改。")
    elif choice == "2":
        if apply_monkey_patch():
            print("\n✅ 兼容性补丁已应用！")
            print("请使用 'python start_gui.py' 启动GUI")
    elif choice == "3":
        if fix_chromadb():
            print("\n✅ chromadb已更新！")
            print("请重新运行程序尝试是否已解决问题。")
    else:
        print("无效的选择")

if __name__ == "__main__":
    main()
