"""
RAG知识库系统 - 备选简单可视化界面
使用原生tkinter创建简单易用的图形界面
"""
import os
import sys
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox

class SimpleRAGTkApp:
    def __init__(self, root):
        """初始化应用"""
        self.root = root
        self.root.title("RAG知识库问答系统")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        self.agent = None
        self.status = "未初始化"
        
        self.create_widgets()
        self.update_status("就绪，请初始化知识库", "blue")
        
    def create_widgets(self):
        """创建GUI组件"""
        # 标题
        title_frame = tk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="RAG知识库问答系统", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=5)
        
        # 状态栏
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10)
        
        status_label = tk.Label(status_frame, text="系统状态:")
        status_label.pack(side=tk.LEFT)
        
        self.status_text = tk.Label(
            status_frame, 
            text=self.status, 
            fg="blue",
            width=50
        )
        self.status_text.pack(side=tk.LEFT, padx=5)
        
        # 分隔线
        separator1 = ttk.Separator(self.root, orient='horizontal')
        separator1.pack(fill=tk.X, padx=10, pady=5)
        
        # 聊天区域框架
        chat_frame = ttk.LabelFrame(self.root, text="对话区域")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 聊天历史
        self.chat_history = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=("Arial", 10),
            bg="#F8F8F8"
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_history.config(state=tk.DISABLED)  # 设为只读
        
        # 问题输入区域
        question_label = tk.Label(chat_frame, text="问题:")
        question_label.pack(anchor=tk.W, padx=5)
        
        self.question_input = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=3,
            font=("Arial", 10)
        )
        self.question_input.pack(fill=tk.X, padx=5, pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(chat_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.send_btn = tk.Button(
            button_frame,
            text="发送问题",
            bg="#007BFF",
            fg="white",
            width=15,
            command=self.send_question
        )
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="清空对话",
            width=15,
            command=self.clear_chat
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.time_label = tk.Label(
            button_frame,
            text="",
            width=20
        )
        self.time_label.pack(side=tk.RIGHT, padx=5)
        
        # 分隔线
        separator2 = ttk.Separator(self.root, orient='horizontal')
        separator2.pack(fill=tk.X, padx=10, pady=5)
        
        # 操作按钮区域
        operations_frame = ttk.LabelFrame(self.root, text="操作")
        operations_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ops_button_frame = tk.Frame(operations_frame)
        ops_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.init_btn = tk.Button(
            ops_button_frame,
            text="初始化知识库",
            bg="#28a745",
            fg="white",
            width=15,
            command=self.initialize_agent
        )
        self.init_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.fix_btn = tk.Button(
            ops_button_frame,
            text="修复兼容性",
            bg="#ffc107",
            fg="black",
            width=15,
            command=self.run_fix_compatibility
        )
        self.fix_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.exit_btn = tk.Button(
            ops_button_frame,
            text="退出",
            bg="#dc3545",
            fg="white",
            width=15,
            command=self.root.destroy
        )
        self.exit_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 使用说明
        help_text = "使用说明: 点击'初始化知识库'按钮加载知识库，然后在问题框中输入问题，点击'发送问题'获取回答。"
        help_label = tk.Label(
            self.root,
            text=help_text,
            fg="gray",
            font=("Arial", 9)
        )
        help_label.pack(padx=10, pady=5)
        
        # 绑定回车键
        self.question_input.bind("<Control-Return>", lambda event: self.send_question())
    
    def update_status(self, status_msg, color="blue"):
        """更新状态消息"""
        self.status = status_msg
        self.status_text.config(text=status_msg, fg=color)
    
    def append_to_chat(self, text, is_user=False):
        """添加消息到聊天历史"""
        self.chat_history.config(state=tk.NORMAL)  # 临时解除只读
        
        if self.chat_history.get("1.0", tk.END).strip():
            self.chat_history.insert(tk.END, "\n\n")
            
        prefix = "🙋 您: " if is_user else "🤖 系统: "
        self.chat_history.insert(tk.END, prefix + text)
        
        # 滚动到底部
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)  # 恢复只读
    
    def initialize_agent(self):
        """初始化RAG代理"""
        self.update_status("正在初始化知识库...", "orange")
        
        # 使用线程避免界面冻结
        threading.Thread(target=self._initialize_agent_thread, daemon=True).start()
    
    def _initialize_agent_thread(self):
        """在线程中初始化RAG代理"""
        try:
            from src.agents.rag_agent import RAGAgent
            
            # 目录配置
            docs_dir = "docs"
            db_dir = "vector_db"
            
            # 检查文档目录
            if not os.path.exists(docs_dir) or len(os.listdir(docs_dir)) == 0:
                self.update_status("错误: 没有找到任何文档。请先运行导入文档选项。", "red")
                return
                
            # 检查是否需要初始化向量数据库
            need_init = not os.path.exists(db_dir) or len(os.listdir(db_dir) if os.path.isdir(db_dir) else []) == 0
            
            try:
                status_msg = "正在构建新知识库..." if need_init else "正在加载已有知识库..."
                self.update_status(status_msg, "orange")
                
                self.agent = RAGAgent(
                    docs_dir=docs_dir,
                    persist_dir=db_dir,
                    api_base="填写api接口",
                    api_key="填写api密钥"
                )
                
                self.update_status("知识库已成功加载！", "green")
                
            except Exception as e:
                error_msg = f"{'构建' if need_init else '加载'}知识库出错: {str(e)}"
                self.update_status(error_msg, "red")
                messagebox.showerror("初始化错误", error_msg)
                
        except ImportError as e:
            error_msg = f"导入RAGAgent失败: {str(e)}。请先修复兼容性问题。"
            self.update_status(error_msg, "red")
            messagebox.showerror("导入错误", error_msg)
    
    def run_fix_compatibility(self):
        """运行修复兼容性的脚本"""
        self.update_status("正在修复兼容性问题...", "orange")
        
        # 使用线程避免界面冻结
        threading.Thread(target=self._fix_compatibility_thread, daemon=True).start()
    
    def _fix_compatibility_thread(self):
        """在线程中运行修复兼容性的脚本"""
        try:
            script_path = os.path.join("tools", "fix_compatibility.py")
            if not os.path.exists(script_path):
                error_msg = f"错误: 找不到修复脚本 {script_path}"
                self.update_status(error_msg, "red")
                messagebox.showerror("脚本错误", error_msg)
                return
            
            import subprocess
            result = subprocess.run([sys.executable, script_path], check=True)
            if result.returncode == 0:
                self.update_status("兼容性问题已修复！请重新初始化知识库。", "green")
                messagebox.showinfo("修复成功", "兼容性问题已修复！请重新初始化知识库。")
            else:
                self.update_status("修复过程中出错。", "red")
                messagebox.showerror("修复失败", "修复过程中出错。")
        except Exception as e:
            error_msg = f"修复过程出错: {str(e)}"
            self.update_status(error_msg, "red")
            messagebox.showerror("修复错误", error_msg)
    
    def send_question(self):
        """发送问题并获取回答"""
        question = self.question_input.get("1.0", tk.END).strip()
        if not question:
            return
        
        # 清空输入框
        self.question_input.delete("1.0", tk.END)
        self.append_to_chat(question, is_user=True)
        
        # 在线程中处理查询
        threading.Thread(target=self.query_in_thread, args=(question,), daemon=True).start()
    
    def query_in_thread(self, question):
        """在独立线程中查询，避免界面冻结"""
        try:
            if not self.agent:
                self.append_to_chat("请先初始化知识库！")
                self.update_status("请先初始化知识库", "red")
                return
            
            start_time = time.time()
            self.update_status("正在查询知识库...", "blue")
            
            try:
                # 使用查询方法
                response = self.agent.query(question)
                
                # 计算耗时
                end_time = time.time()
                query_time = end_time - start_time
                
                # 更新界面
                self.append_to_chat(response)
                self.time_label.config(text=f"查询用时: {query_time:.2f}秒")
                self.update_status("就绪", "green")
            
            except Exception as e:
                error_msg = f"查询出错: {str(e)}"
                self.append_to_chat(error_msg)
                self.update_status(error_msg, "red")
            
        except Exception as e:
            error_msg = f"线程错误: {str(e)}"
            self.update_status(error_msg, "red")
    
    def clear_chat(self):
        """清空聊天历史"""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.time_label.config(text="")

def main():
    """主函数"""
    root = tk.Tk()
    app = SimpleRAGTkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
