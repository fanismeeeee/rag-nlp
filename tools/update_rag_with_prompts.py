"""
更新RAGAgent类以使用定义好的提示词模板
"""
import os
import sys
import re

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def update_rag_agent_with_prompts():
    """更新RAGAgent类以使用定义好的提示词模板"""
    file_path = os.path.join(project_root, "src", "agents", "rag_agent.py")
    
    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 检查是否已经导入了提示词模板
        if "from src.prompts.rag_prompts import RAGPromptTemplates" in content:
            print("RAGAgent已经包含提示词模板，无需更新")
            return True
        
        # 添加导入语句
        import_pattern = r"from langchain.*?\n"
        match = re.search(import_pattern, content)
        if match:
            position = match.end()
            updated_content = content[:position] + "\nfrom src.prompts.rag_prompts import RAGPromptTemplates\n" + content[position:]
            
            # 更新query方法，使用提示词模板
            query_method_pattern = r"def query\(self, question\):.*?return response"
            
            # 使用提示词模板替换简单的提示
            updated_query_method = """def query(self, question):
        '''查询知识库并返回回答'''
        if not self.vector_store:
            return "知识库尚未初始化，请先加载文档"
            
        # 从知识库中检索相关文档
        docs = self.vector_store.similarity_search(question, k=3)
        
        # 构建上下文
        context = "\\n\\n".join([doc.page_content for doc in docs])
        
        # 使用提示词模板
        template = RAGPromptTemplates.get_chinese_qa_template()
        prompt = template.format(context=context, question=question)
        
        # 调用LLM
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm_api(messages)
        return response"""
            
            # 替换query方法
            updated_content = re.sub(query_method_pattern, updated_query_method, updated_content, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f"已更新 {file_path}，添加了提示词模板支持")
            return True
        else:
            print(f"无法在 {file_path} 中找到合适的位置添加导入语句")
            return False
    
    except Exception as e:
        print(f"更新文件时出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("正在更新RAGAgent以支持提示词模板...")
    success = update_rag_agent_with_prompts()
    if success:
        print("✅ 更新成功！RAGAgent现在支持提示词模板")
    else:
        print("❌ 更新失败，请手动修改RAGAgent")
