"""
改进版的RAG代理query方法修复工具
使用更精确的方式修复chat_history缺失问题，保留原始缩进
"""
import os
import sys
import re

def show_header():
    """显示脚本标题"""
    print("="*60)
    print("  改进版查询方法修复工具")
    print("="*60)

def fix_rag_agent():
    """修复RAG代理中的query方法"""
    rag_agent_path = os.path.join("src", "agents", "rag_agent.py")
    
    if not os.path.exists(rag_agent_path):
        print(f"错误: 找不到文件 {rag_agent_path}")
        return False
        
    try:
        # 读取当前内容
        with open(rag_agent_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # 找到query方法并修改invoke调用行
        in_query_method = False
        found_invoke = False
        modified_lines = []
        
        for line in lines:
            if line.strip().startswith("def query(self,"):
                in_query_method = True
                modified_lines.append(line)
            elif in_query_method and "self.qa_chain.invoke" in line:
                # 找到invoke调用行
                # 检查是否已经包含chat_history参数
                if "chat_history" not in line:
                    # 保持原有的缩进
                    indent = line[:len(line) - len(line.lstrip())]
                    
                    # 修改行，添加chat_history参数
                    if '{"question": question}' in line:
                        new_line = line.replace(
                            '{"question": question}',
                            '{"question": question, "chat_history": []}'
                        )
                        modified_lines.append(new_line)
                    else:
                        # 如果无法精确匹配，尝试使用正则表达式
                        modified_lines.append(line)
                        print("警告: 无法精确定位invoke参数，可能需要手动修复")
                    
                    found_invoke = True
                else:
                    # 已经包含chat_history参数，无需修改
                    modified_lines.append(line)
                    found_invoke = True
            else:
                modified_lines.append(line)
                
                # 如果离开了query方法的范围，重置状态
                if in_query_method and line.strip() == "" and len(modified_lines) > 0:
                    # 检查前一行是否为方法结束（return语句）
                    prev_line = modified_lines[-2] if len(modified_lines) >= 2 else ""
                    if "return" in prev_line:
                        in_query_method = False
        
        # 如果没有找到invoke调用行，尝试直接创建一个新的query方法
        if not found_invoke:
            print("无法定位现有的invoke调用，将尝试替换整个query方法...")
            
            # 重置修改
            modified_lines = []
            new_method_added = False
            
            for line in lines:
                if line.strip().startswith("def query(self,") and not new_method_added:
                    # 找到方法定义，跳过整个方法直到下一个方法定义
                    skip_until_next_def = True
                    indent = line[:len(line) - len(line.lstrip())]
                    
                    # 添加新的query方法
                    modified_lines.append(f"{indent}def query(self, question: str) -> str:\n")
                    modified_lines.append(f"{indent}    \"\"\"\n")
                    modified_lines.append(f"{indent}    使用问题查询RAG系统。\n")
                    modified_lines.append(f"{indent}    \n")
                    modified_lines.append(f"{indent}    Args:\n")
                    modified_lines.append(f"{indent}        question: 用户问题\n")
                    modified_lines.append(f"{indent}        \n")
                    modified_lines.append(f"{indent}    Returns:\n")
                    modified_lines.append(f"{indent}        str: 回答文本\n")
                    modified_lines.append(f"{indent}    \"\"\"\n")
                    modified_lines.append(f"{indent}    # 使用invoke方法，提供空的chat_history\n")
                    modified_lines.append(f"{indent}    response = self.qa_chain.invoke({{'question': question, 'chat_history': []}})\n")
                    modified_lines.append(f"{indent}    return response[\"answer\"]\n")
                    modified_lines.append("\n")
                    new_method_added = True
                elif line.strip().startswith("def ") and skip_until_next_def:
                    # 找到下一个方法定义，停止跳过
                    skip_until_next_def = False
                    modified_lines.append(line)
                elif not skip_until_next_def:
                    modified_lines.append(line)
        
        # 写回文件
        with open(rag_agent_path, "w", encoding="utf-8") as f:
            f.writelines(modified_lines)
            
        print(f"✓ 已更新 {rag_agent_path} 中的query方法")
        return True
            
    except Exception as e:
        print(f"修复query方法时出错: {str(e)}")
        return False

def main():
    """主函数"""
    show_header()
    
    print("使用改进的方法修复RAG代理中的query方法...")
    
    success = fix_rag_agent()
    
    if success:
        print("\n✅ query方法已修复！现在可以尝试重新运行系统了。")
    else:
        print("\n❌ 修复失败！请手动检查rag_agent.py文件。")
        print("\n手动修复方法: 打开src/agents/rag_agent.py文件,")
        print("在query方法中将:")
        print('  response = self.qa_chain.invoke({"question": question})')
        print("修改为:")
        print('  response = self.qa_chain.invoke({"question": question, "chat_history": []})')

if __name__ == "__main__":
    main()
