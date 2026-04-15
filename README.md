# 🤖 RAG PDF Chatbot - Complete Guide

A production-ready Retrieval-Augmented Generation (RAG) system that enables intelligent Q&A over PDF documents using modern LLMs.

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Deployment Options](#deployment-options)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **📄 Multi-PDF Support**: Process multiple PDFs simultaneously
- **🔍 Semantic Search**: Vector-based retrieval using embeddings
- **🧠 Multiple LLM Options**: OpenAI, Ollama (local), HuggingFace
- **💾 Vector Store Options**: FAISS or Chroma
- **⚡ Production Ready**: Optimized, cached, and scalable
- **🎨 Beautiful UI**: Interactive Streamlit interface
- **📊 Source Attribution**: Know where answers come from
- **🔧 Fully Customizable**: Adjust all parameters via UI

## 🚀 Quick Start

### Option 1: Google Colab (Easiest - No Setup Required!)

1. Open the Colab notebook:
   - Click on `colab_setup.ipynb` or access via: https://colab.research.google.com

2. Run cells sequentially:
   - Cell 1: Install dependencies
   - Cell 2-4: Create project files
   - Cell 5: Launch Streamlit with public URL

3. Access your app via the generated ngrok URL

### Option 2: Local Development

```bash
# Clone or download the project
git clone <your-repo-url>
cd rag-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the app
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` in your browser.

### Option 3: Docker (Recommended for Production)

```bash
# Build Docker image
docker build -t rag-chatbot .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  rag-chatbot

# Access at http://localhost:8501
```

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────┐
│         User Interface (Streamlit)      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         RAG Pipeline Manager            │
│  - Session State Management             │
│  - Chat History                         │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┬────────────┐
        │                 │            │
┌───────▼──────┐  ┌──────▼───┐  ┌────▼──────┐
│   Document   │  │ Vector   │  │    LLM    │
│   Processing │  │  Store   │  │  Provider │
│              │  │          │  │           │
│ • PDF Load   │  │• FAISS   │  │• OpenAI   │
│ • Chunking   │  │• Chroma  │  │• Ollama   │
│ • Splitting  │  │• Index   │  │• HF Model │
└──────────────┘  └──────────┘  └───────────┘
        │              │              │
        └──────────────┬──────────────┘
                       │
┌──────────────────────▼─────────────────┐
│      Embedding Model                   │
│  (sentence-transformers/all-MiniLM)   │
└────────────────────────────────────────┘
```

### Data Flow

```
User Query
    │
    ▼
[Embedding] ──► [Vector Search] ──► [Context Retrieval]
    │                                    │
    └────────────────┬───────────────────┘
                     │
                     ▼
            [LLM with Context]
                     │
                     ▼
           [Response + Sources]
                     │
                     ▼
              [User Display]
```

## 📦 Project Structure

```
rag-chatbot/
├── streamlit_app.py          # Main Streamlit application
├── rag_pipeline.py           # Core RAG pipeline logic
├── utils.py                  # Utility functions & helpers
├── requirements.txt          # Python dependencies
├── colab_setup.ipynb        # Google Colab notebook
├── Dockerfile               # Docker configuration
├── .env.example            # Example environment variables
├── deployment_guide.md     # Detailed deployment guide
└── README.md              # This file
```

## ⚙️ Configuration

### Environment Variables

Create `.env` file:

```env
# LLM Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Alternative LLM providers
HUGGINGFACE_API_KEY=hf_your-key
OLLAMA_HOST=http://localhost:11434

# Vector Store
VECTOR_STORE_TYPE=faiss  # or 'chroma'
VECTOR_STORE_PATH=./vector_store

# RAG Settings
CHUNK_SIZE=512
CHUNK_OVERLAP=50
TOP_K_RETRIEVAL=3
```

### Model Selection

#### OpenAI (Recommended for Production)
- **Pros**: Highest quality, easiest setup
- **Cons**: Costs money ($0.0015/1K tokens)
- **Setup**:
  ```bash
  export OPENAI_API_KEY=sk-your-key
  ```

#### Ollama (Local, Free)
- **Pros**: Free, private, offline
- **Cons**: Slower, requires GPU
- **Setup**:
  ```bash
  # Install Ollama from https://ollama.ai
  ollama pull mistral
  # Start: ollama serve
  ```

#### HuggingFace (Local Models)
- **Pros**: Open source, many models available
- **Cons**: Memory intensive
- **Setup**:
  ```bash
  # Automatically downloads model on first use
  ```

## 🌐 Deployment Options

### 1. **Streamlit Cloud** (Free, Recommended)

Easiest deployment option.

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to https://streamlit.io/cloud
# 3. Click "New app"
# 4. Select your repository
# 5. Set environment variables in settings
```

**Pros**: Free, automatic updates, easy management
**Cons**: Limited compute, cold starts

### 2. **Heroku** ($5-50/month)

```bash
# Install Heroku CLI
brew install heroku

# Login and create app
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Pros**: Simple, affordable, good performance
**Cons**: Dyno sleep for free tier

### 3. **AWS EC2** (Production)

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. SSH into instance
ssh -i key.pem ubuntu@instance-ip

# 3. Install dependencies
sudo apt update && sudo apt install python3-pip python3-venv

# 4. Clone and setup
git clone <repo>
cd rag-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Run with PM2 or systemd
pip install pm2
pm2 start "streamlit run streamlit_app.py"

# 6. Setup Nginx reverse proxy
sudo apt install nginx
# Configure proxy settings

# 7. Get SSL certificate
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

**Pros**: Full control, scalable, good for production
**Cons**: More setup, costs money

### 4. **Google Cloud Run** (Serverless)

```bash
# Build and push Docker image
docker build -t gcr.io/PROJECT_ID/rag-chatbot .
docker push gcr.io/PROJECT_ID/rag-chatbot

# Deploy
gcloud run deploy rag-chatbot \
  --image gcr.io/PROJECT_ID/rag-chatbot \
  --platform managed \
  --set-env-vars OPENAI_API_KEY=sk-...
```

**Pros**: Serverless, auto-scaling, pay-per-use
**Cons**: Cold starts, pricing complexity

### 5. **RunPod / Vast.ai** (GPU Inference)

For fine-tuned models and heavy computations:

```bash
# 1. Create account on RunPod.io or Vast.ai
# 2. Rent GPU instance (e.g., RTX 4090)
# 3. Install and run application
# 4. Expose via ngrok or custom networking
```

## 📝 Usage Examples

### Basic Question Answering

```
User: "What are the main findings in this document?"
Assistant: [Context-aware answer from PDF]
Sources: 
- document.pdf (Page 3): "The main findings show..."
```

### Multi-Document Queries

```
User: "Compare the methodologies used in both papers"
Assistant: [Retrieves and compares from multiple PDFs]
```

### Specific Information Retrieval

```
User: "What is the author's name and affiliation?"
Assistant: [Extracts from document metadata]
```

## 🔧 Advanced Configuration

### Custom Prompts

Edit `rag_pipeline.py` in `_create_qa_chain()`:

```python
custom_prompt_template = """
You are an expert at answering questions based on documents.
Context: {context}
Question: {question}
Answer in a clear, structured way:
"""
```

### Multiple Vector Stores

```python
# Use Chroma for persistence
vector_store_type = "chroma"
self.vector_store = Chroma.from_documents(
    chunks,
    self.embeddings,
    persist_directory="./chroma_db"
)
```

### Fine-tune Retrieval

```python
# Adjust retrieval parameters
self.retriever = self.vector_store.as_retriever(
    search_type="mmr",  # Maximum Marginal Relevance
    search_kwargs={"k": 5, "lambda_mult": 0.25}
)
```

## 🐛 Troubleshooting

### Issue: "API Key not found"
```bash
# Solution: Set environment variable
export OPENAI_API_KEY=sk-your-key-here
```

### Issue: Out of Memory
```python
# Reduce chunk size
chunk_size = 256

# Use lighter embedding model
embedding_model = "distiluse-base-multilingual-cased-v2"

# Reduce top_k
top_k = 2
```

### Issue: Slow Response Time
```python
# Use faster model
model_name = "gpt-3.5-turbo"  # Instead of gpt-4

# Reduce chunk overlap
chunk_overlap = 0

# Cache embeddings
# Enable Streamlit caching with @st.cache_resource
```

### Issue: Poor Quality Answers
```python
# Increase top_k for more context
top_k = 5

# Reduce temperature for more focused answers
temperature = 0.3

# Use longer chunks
chunk_size = 1024

# Use better embedding model
embedding_model = "all-mpnet-base-v2"
```

## 📊 Performance Metrics

Typical performance on consumer hardware:

| Metric | Value |
|--------|-------|
| PDF Processing | ~5s for 10-page PDF |
| Vector Store Build | ~2s for 100 chunks |
| Query Response | ~2-5s (depends on LLM) |
| Memory Usage | ~2-4GB (CPU) |
| GPU Memory | ~8GB (with GPU) |

## 🤝 Contributing

Contributions are welcome! 

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

MIT License - See LICENSE file for details

## 🆘 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **LangChain Docs**: https://python.langchain.com
- **OpenAI API Docs**: https://platform.openai.com/docs
- **GitHub Issues**: Report bugs here

## 🎯 Project Goals

This project demonstrates:
- ✅ RAG (Retrieval-Augmented Generation) implementation
- ✅ Vector database usage (FAISS/Chroma)
- ✅ LLM integration (OpenAI/HuggingFace)
- ✅ Production deployment strategies
- ✅ Streamlit web application development
- ✅ Full-stack LLM application architecture

Perfect for **Deep Learning course projects** and **LLM engineering portfolios**!

---

**Built with ❤️ for the LLM engineering community**
