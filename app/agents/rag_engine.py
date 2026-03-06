import os
from typing import List, Dict, Any
import pandas as pd
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class SECopsRAGEngine:
    def __init__(self, api_key: str = None):
        """Initializes the RAG Engine with OpenAI Embeddings."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for the RAG Embedding Engine.")
            
        # Using the standard text-embedding-3-small or fallback to ada-002
        self.embeddings = OpenAIEmbeddings(
            api_key=self.api_key,
            model="text-embedding-3-small"
        )
        self.vector_store = None

    def _dataframe_to_documents(self, df: pd.DataFrame, doc_type: str) -> List[Document]:
        """Converts a Pandas DataFrame into LangChain Document objects."""
        documents = []
        for _, row in df.iterrows():
            # Condense row data into a single searchable string
            row_dict = row.to_dict()
            page_content = "\n".join([f"{k}: {v}" for k, v in row_dict.items()])
            
            # Extract metadata
            metadata = {"source": doc_type}
            if doc_type == "KEDB":
                metadata["id"] = row.get("Error_Code", "Unknown")
            else:
                metadata["id"] = row.get("Ticket_ID", "Unknown")
                
            doc = Document(page_content=page_content, metadata=metadata)
            documents.append(doc)
            
        return documents

    def ingest_data(self, kedb_df: pd.DataFrame, tickets_df: pd.DataFrame):
        """Vectorizes and indexes the synthetic datasets into FAISS."""
        kedb_docs = self._dataframe_to_documents(kedb_df, "KEDB")
        ticket_docs = self._dataframe_to_documents(tickets_df, "TICKET")
        
        all_docs = kedb_docs + ticket_docs
        
        # Build the purely in-memory FAISS index
        self.vector_store = FAISS.from_documents(all_docs, self.embeddings)

    def retrieve_context(self, query: str, top_k: int = 4) -> str:
        """Runs a similarity search and returns the top K most relevant documents as a string."""
        if not self.vector_store:
            return "No vector store initialized. Please ingest data first."
            
        results = self.vector_store.similarity_search(query, k=top_k)
        
        context_string = "--- RETRIEVED KNOWLEDGE BASE CONTEXT ---\n\n"
        for i, doc in enumerate(results):
            context_string += f"[Document {i+1} | Source: {doc.metadata.get('source')} | ID: {doc.metadata.get('id')}]\n"
            context_string += doc.page_content + "\n\n"
            
        return context_string
