"""
Utility functions for RAG PDF Chatbot
Includes display helpers, PDF processing, and formatting utilities
"""

import streamlit as st
from typing import List, Tuple
from pathlib import Path
import PyPDF2
from datetime import datetime


def display_sources(sources: List[Tuple[str, str]]):
    """
    Display source documents in a formatted box
    
    Args:
        sources: List of (filename, content) tuples
    """
    if not sources:
        return
    
    with st.container():
        st.markdown("### 📚 Source Documents")
        
        for i, (source, content) in enumerate(sources, 1):
            with st.expander(f"Source {i}: {Path(source).name if source else 'Unknown'}"):
                st.text(content)
                if source:
                    st.caption(f"📄 {source}")


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract all text from a PDF file
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting PDF: {e}")
        return ""


def get_pdf_page_count(pdf_path: str) -> int:
    """
    Get total page count of a PDF
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Number of pages
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)
    except Exception as e:
        return 0


def format_chat_timestamp(timestamp: datetime) -> str:
    """
    Format timestamp for display
    
    Args:
        timestamp: datetime object
        
    Returns:
        Formatted timestamp string
    """
    return timestamp.strftime("%H:%M:%S")


def estimate_tokens(text: str) -> int:
    """
    Rough estimate of token count (1 token ≈ 4 characters)
    
    Args:
        text: Text to estimate
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def highlight_keywords(text: str, keywords: List[str]) -> str:
    """
    Highlight keywords in text
    
    Args:
        text: Text to process
        keywords: List of keywords to highlight
        
    Returns:
        Text with highlighted keywords
    """
    for keyword in keywords:
        text = text.replace(keyword, f"**{keyword}**")
    return text


def create_summary(text: str, max_length: int = 100) -> str:
    """
    Create a summary of text
    
    Args:
        text: Text to summarize
        max_length: Maximum summary length
        
    Returns:
        Summary text
    """
    sentences = text.split('.')
    summary = ""
    
    for sentence in sentences:
        if len(summary) + len(sentence) <= max_length:
            summary += sentence + "."
        else:
            break
    
    return summary.strip()


class DocumentMetadata:
    """Handle document metadata and statistics"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.filename = Path(pdf_path).name
        self.page_count = get_pdf_page_count(pdf_path)
        self.upload_time = datetime.now()
    
    def get_info_dict(self) -> dict:
        """Get metadata as dictionary"""
        return {
            "filename": self.filename,
            "path": self.pdf_path,
            "pages": self.page_count,
            "uploaded_at": self.upload_time.isoformat()
        }
    
    def display_in_streamlit(self):
        """Display metadata in Streamlit"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("File Name", self.filename[:20] + "..." if len(self.filename) > 20 else self.filename)
        with col2:
            st.metric("Pages", self.page_count)
        with col3:
            st.metric("Uploaded", self.upload_time.strftime("%H:%M"))


def validate_pdf(uploaded_file) -> bool:
    """
    Validate uploaded PDF file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check file extension
        if not uploaded_file.name.lower().endswith('.pdf'):
            st.error("File must be a PDF")
            return False
        
        # Check file size (max 50MB)
        max_size = 50 * 1024 * 1024
        if len(uploaded_file.getvalue()) > max_size:
            st.error("File size exceeds 50MB limit")
            return False
        
        # Try to read as PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        if len(pdf_reader.pages) == 0:
            st.error("PDF has no pages")
            return False
        
        return True
        
    except Exception as e:
        st.error(f"Invalid PDF: {e}")
        return False


def save_chat_history(chat_history: List[dict], filename: str = "chat_history.json"):
    """
    Save chat history to JSON file
    
    Args:
        chat_history: List of chat messages
        filename: Output filename
    """
    import json
    
    # Convert datetime objects to strings
    serializable_history = []
    for msg in chat_history:
        msg_copy = msg.copy()
        if "timestamp" in msg_copy:
            msg_copy["timestamp"] = msg_copy["timestamp"].isoformat()
        serializable_history.append(msg_copy)
    
    with open(filename, 'w') as f:
        json.dump(serializable_history, f, indent=2)


def load_chat_history(filename: str = "chat_history.json") -> List[dict]:
    """
    Load chat history from JSON file
    
    Args:
        filename: Input filename
        
    Returns:
        List of chat messages
    """
    import json
    from pathlib import Path
    
    if not Path(filename).exists():
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)


# Performance monitoring utilities
class PerformanceMonitor:
    """Monitor RAG pipeline performance"""
    
    def __init__(self):
        self.metrics = {
            "queries": 0,
            "total_response_time": 0,
            "avg_retrieval_time": 0,
            "errors": 0
        }
    
    def record_query(self, response_time: float, retrieval_time: float, success: bool = True):
        """Record query metrics"""
        self.metrics["queries"] += 1
        self.metrics["total_response_time"] += response_time
        self.metrics["avg_retrieval_time"] += retrieval_time
        
        if not success:
            self.metrics["errors"] += 1
    
    def get_stats(self) -> dict:
        """Get performance statistics"""
        queries = self.metrics["queries"]
        if queries == 0:
            return self.metrics
        
        return {
            **self.metrics,
            "avg_response_time": self.metrics["total_response_time"] / queries,
            "error_rate": self.metrics["errors"] / queries
        }
    
    def display_in_streamlit(self):
        """Display metrics in Streamlit"""
        stats = self.get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Queries", stats["queries"])
        with col2:
            st.metric("Avg Response Time", f"{stats.get('avg_response_time', 0):.2f}s")
        with col3:
            st.metric("Error Rate", f"{stats.get('error_rate', 0):.1%}")
        with col4:
            st.metric("Avg Retrieval Time", f"{stats.get('avg_retrieval_time', 0):.2f}s")
