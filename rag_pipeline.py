
"""RAG Pipeline Implementation"""
import os
from typing import List, Tuple, Optional
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

class RAGPipeline:
    def __init__(self, model_name="gpt-3.5-turbo", embedding_model="sentence-transformers/all-MiniLM-L6-v2",
                 provider="openai", api_key=None, chunk_size=512, chunk_overlap=50, top_k=3):
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.provider = provider
        self.api_key = api_key
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k

        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.retriever = None
        self.qa_chain = None

        self._initialize_embeddings()
        self._initialize_llm()

    def _initialize_embeddings(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        print(f"✅ Embeddings initialized: {self.embedding_model}")

    def _initialize_llm(self):
        if self.provider == "openai":
            self.llm = OpenAI(openai_api_key=self.api_key, model_name=self.model_name, temperature=0.7)
            print(f"✅ OpenAI LLM initialized: {self.model_name}")

    def build_vector_store(self, pdf_paths: List[str]):
        documents = []
        for pdf_path in pdf_paths:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            documents.extend(docs)

        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = splitter.split_documents(documents)

        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": self.top_k})
        self._create_qa_chain()
        print(f"✅ Vector store built with {len(chunks)} chunks")

    def _create_qa_chain(self):
        prompt = PromptTemplate(template="Use context to answer: {context}\nQuestion: {question}\nAnswer:",
                              input_variables=["context", "question"])
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff",
                                                    retriever=self.retriever, return_source_documents=True)

    def query(self, question: str, temperature: float = 0.7) -> Tuple[str, List]:
        response = self.qa_chain({"query": question})
        answer = response.get("result", "")
        sources = [(doc.metadata.get("source"), doc.page_content[:200]) for doc in response.get("source_documents", [])]
        return answer, sources
