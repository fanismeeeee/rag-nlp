#!/usr/bin/env python
"""
RAG知识库系统启动器 - 应用NumPy兼容性补丁后启动GUI
"""
import os
import sys
import importlib.util

def apply_numpy_patch():
    """应用NumPy兼容性补丁"""
    import numpy as np
    
    # 如果是NumPy 2.0+并且没有float_属性，添加别名
    if not hasattr(np, 'float_') and np.__version__.startswith('2.'):
        # 创建别名以兼容旧代码
        np.float_ = np.float64
        print("已应用NumPy 2.0兼容性补丁: np.float_ -> np.float64")

def apply_chromadb_patch():
    """修复chromadb中的类型问题"""
    try:
        # 尝试在chromadb导入前修复类型问题
        import sys
        from unittest.mock import MagicMock
        import numpy as np
        
        # 确保numpy有float_属性
        if not hasattr(np, 'float_'):
            np.float_ = np.float64
        
        # 修补其他可能的类型
        if not hasattr(np, 'int_'):
            np.int_ = np.int64
            
        print("已准备好chromadb的兼容性环境")
    except Exception as e:
        print(f"应用chromadb补丁时出错: {str(e)}")

def main():
    """主函数"""
    print("="*60)
    print("  RAG知识库系统启动器")
    print("="*60)
    
    # 应用NumPy补丁
    apply_numpy_patch()
    
    # 应用chromadb补丁
    apply_chromadb_patch()
    
    print("\n正在启动图形界面...")
    print("-"*60)
    
    # 导入并运行GUI
    import simple_gui_tk
    simple_gui_tk.main()

if __name__ == "__main__":
    main()
