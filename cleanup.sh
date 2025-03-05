# 删除重复的README（保留更规范的版本）
rm "/d:/code/python/rag-knowledge-base/README.md"

# 整合requirements.txt文件
cat << 'EOF' > "/d:/code/python/rag-knowledge-base/requirements.txt"
# 整合后的依赖项
langchain>=0.0.267
langchain-community
python-dotenv
torch
transformers
sentence-transformers
openai>=1.0.0
chromadb>=0.4.15
PyPDF2>=3.0.0
python-docx>=0.8.11
tiktoken>=0.4.0
EOF

# 如果不需要本地模型支持，可以删除此文件
rm "/d:/code/python/rag-knowledge-base/src/agents/local_rag_agent.py"
