import os
from typing import List, Dict, Any
import pandas as pd
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import re

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
        self.all_documents = [] # Store raw docs for keyword fallback lookup

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
                metadata["id"] = row.get("KE ID", "Unknown")
            else:
                metadata["id"] = row.get("Ticket ID", "Unknown")
                
            doc = Document(page_content=page_content, metadata=metadata)
            documents.append(doc)
            
        return documents

    def ingest_data(self, kedb_df: pd.DataFrame, tickets_df: pd.DataFrame):
        """Vectorizes and indexes the synthetic datasets into FAISS."""
        kedb_docs = self._dataframe_to_documents(kedb_df, "KEDB")
        ticket_docs = self._dataframe_to_documents(tickets_df, "TICKET")
        
        all_docs = kedb_docs + ticket_docs
        self.all_documents = all_docs
        
        # Build the purely in-memory FAISS index
        self.vector_store = FAISS.from_documents(all_docs, self.embeddings)

    def retrieve_context(self, query: str, top_k: int = 4) -> str:
        """
        Runs a Hybrid Retrieval search:
        1. Alphanumeric Keyword Scan (Exact match for IDs like KE-, CHG-, INC-, SR-)
        2. Semantic Similarity Search (FAISS)
        Merges results to ensure technical IDs are never missed.
        """
        if not self.vector_store:
            return "No vector store initialized. Please ingest data first."
            
        # 1. Keyword ID Extraction (Regex)
        # Matches patterns like KE-001, CHG1234567, INC9876543, SR1122334
        id_pattern = r"(KE-\d+|CHG\d+|INC\d+|SR\d+|KE \d+)"
        found_ids = re.findall(id_pattern, query, re.IGNORECASE)
        found_ids = [fid.upper().replace(" ", "-") if fid.upper().startswith("KE") else fid.upper() for fid in found_ids]

        keyword_results = []
        if found_ids:
            # Search for exact ID matches in metadata
            for doc in self.all_documents:
                doc_id = str(doc.metadata.get("id", "")).upper()
                if any(fid in doc_id for fid in found_ids):
                    keyword_results.append(doc)

        # 2. Semantic Search
        semantic_results = self.vector_store.similarity_search(query, k=top_k)
        
        # Merge-Deduplicate results
        # Prioritize keyword matches, then fill with semantic results
        final_results = keyword_results
        seen_ids = {doc.metadata.get("id") for doc in keyword_results}
        
        for doc in semantic_results:
            did = doc.metadata.get("id")
            if did not in seen_ids:
                final_results.append(doc)
                seen_ids.add(did)

        # Truncate to a reasonable context size
        final_results = final_results[:max(top_k, len(keyword_results))]
        
        context_string = "--- RETRIEVED KNOWLEDGE BASE CONTEXT ---\n\n"
        if not final_results:
            context_string += "No specific context matches found in KEDB or Tickets.\n"
        else:
            for i, doc in enumerate(final_results):
                context_string += f"[Document {i+1} | Source: {doc.metadata.get('source')} | ID: {doc.metadata.get('id')}]\n"
                context_string += doc.page_content + "\n\n"
            
        return context_string
