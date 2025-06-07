"""
全新修复版本的RAG代理，解决所有已知问题，优化中文处理能力
"""
import os
from typing import List, Tuple, Any, Dict
from dotenv import load_dotenv

# 使用最新的包路径
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from sentence_transformers import CrossEncoder

# 导入文档加载器工具
from src.utils.document_loaders import get_document_loader

class RAGAgent:
    def __init__(
        self, 
        docs_dir: str = "docs", 
        persist_dir: str = "db", 
        api_base: str = None, 
        api_key: str = None,
        model_name: str = "all-MiniLM-L6-v2",  # 默认使用原始模型，但支持切换
        cross_encoder_model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # 新增参数
    ):
        """
        初始化RAG代理
        
        Args:
            docs_dir: 文档目录
            persist_dir: 向量存储持久化目录
            api_base: API基础URL
            api_key: API密钥
            model_name: 嵌入模型名称，支持多种模型
            cross_encoder_model_name: 交叉编码器模型名称
        """
        load_dotenv()
        
        self.docs_dir = docs_dir
        self.persist_dir = persist_dir
        self.model_name = model_name
        
        # 创建目录（如果不存在）
        os.makedirs(docs_dir, exist_ok=True)
        os.makedirs(persist_dir, exist_ok=True)
        
        # 初始化组件
        # 使用相对路径
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models", model_name)
        
        # 检查模型目录是否存在，如果不存在则使用HuggingFace在线模型
        if not os.path.exists(model_path):
            print(f"本地模型目录 {model_path} 不存在，将使用在线模型 {model_name}")
            self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        else:
            print(f"使用本地模型: {model_path}")
            self.embeddings = HuggingFaceEmbeddings(model_name=model_path)
        
        # 优化的文本分割器，更适合中文处理
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # 对中文，使用较小的块大小
            chunk_overlap=150,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]  # 优先使用中文标点符号分割
        )
        
        # 初始化向量存储
        self.vector_store = self._initialize_vector_store()
        
        # 使用自定义API初始化LLM（如果提供）
        if api_base and api_key:
            self.llm = ChatOpenAI(
                temperature=0.7,
                openai_api_base=api_base,
                openai_api_key=api_key,
                model_name="gpt-3.5-turbo"  # 指定模型名称
            )
        else:
            self.llm = ChatOpenAI(
                temperature=0.7,
                model_name="gpt-3.5-turbo"  # 指定模型名称
            )
        
        # 初始化对话记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"  # 明确指定输出键
        )
        
        # 初始化检索链
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 8}),
            memory=self.memory,
            return_source_documents=True,  # 返回源文档
            verbose=True
        )
        
        # 加载交叉编码器模型
        print(f"加载交叉编码器模型: {cross_encoder_model_name}")
        self.cross_encoder = CrossEncoder(cross_encoder_model_name)

    def _initialize_vector_store(self) -> Chroma:
        """初始化或加载向量存储。"""
        # 检查向量存储是否存在
        if os.path.exists(self.persist_dir) and os.listdir(self.persist_dir):
            print("加载现有向量存储...")
            return Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
        
        print("创建新的向量存储...")
        # 使用增强的文档加载器
        documents = get_document_loader(self.docs_dir)
        
        if not documents:
            print(f"警告: 在{self.docs_dir}目录中未找到任何文档")
            return Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
        
        # 拆分文档
        print(f"处理 {len(documents)} 个文档...")
        splits = self.text_splitter.split_documents(documents)
        print(f"创建了 {len(splits)} 个文本块")
        
        # 创建并持久化向量存储
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        vector_store.persist()
        return vector_store

    def query(self, question: str) -> Dict[str, Any]:
        """
        使用问题查询RAG系统。
        
        Args:
            question: 用户问题
            
        Returns:
            Dict: 包含回答和源文档的字典
        """
        print(f"开始查询: {question}")
        try:
            response = self.qa_chain.invoke({"question": question})
            print(f"查询成功，响应类型: {type(response)}")
            print(f"响应键: {list(response.keys())}")
            
            # 提取答案和源文档
            answer = response.get("answer", "未能获取回答")
            source_docs = response.get("source_documents", [])
            
            print(f"回答: {answer[:100]}...")  # 打印回答的前100个字符
            print(f"找到 {len(source_docs)} 个相关文档")
            
            return {
                "answer": answer,
                "source_documents": source_docs
            }
        except Exception as e:
            print(f"查询出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "answer": f"查询过程中出现错误: {str(e)}",
                "source_documents": []
            }

    def query_with_sources(self, question: str, top_k: int = 15, top_n: int = 8) -> Tuple[str, List[Document]]:
        """
        查询知识库并返回答案和源文档，增加交叉编码器重排序
        Args:
            question: 用户问题
            top_k: 初步召回文档数量
            top_n: 交叉编码器重排序后最终返回文档数量
        Returns:
            tuple: (回答文本, 源文档列表)
        """
        # 嵌入问题
        question_embedding = self.embeddings.embed_query(question)
        # 获取初步相似文档
        docs = self.vector_store.similarity_search_by_vector(question_embedding, k=top_k)
        if not docs:
            return "未找到相关文档", []
        # 用交叉编码器重排序
        pairs = [[question, doc.page_content] for doc in docs]
        scores = self.cross_encoder.predict(pairs)
        # 按分数排序
        doc_score_pairs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        top_docs = [doc for doc, score in doc_score_pairs[:top_n]]
        # 构建提示
        context = "\n\n".join([doc.page_content for doc in top_docs])
        prompt = f"""基于以下信息回答问题。如果信息中找不到答案，请说\"我没有足够的信息来回答这个问题\"。\n请尽可能详细地回答问题，并使用中文回答。\n\n信息:\n{context}\n\n问题: {question}\n\n回答:"""
        response = self.get_completion(prompt)
        return response, top_docs

    def get_completion(self, prompt: str) -> str:
        """使用LLM获取对提示的响应"""
        return self.llm.predict(prompt)

    def ingest_documents(self) -> None:
        """重新初始化带有当前文档的向量存储。"""
        if os.path.exists(self.persist_dir):
            import shutil
            print(f"删除现有向量存储: {self.persist_dir}")
            shutil.rmtree(self.persist_dir)
        self.vector_store = self._initialize_vector_store()
        print("文档导入完成")
        
    def clear_memory(self) -> None:
        """清除对话历史记忆"""
        self.memory.clear()
        print("对话历史已清除")