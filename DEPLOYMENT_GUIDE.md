# 📚 RAG PDF Chatbot - Deployment Guide

Complete instructions for deploying your RAG chatbot to various platforms.

## Table of Contents

1. [Streamlit Cloud](#1-streamlit-cloud-recommended)
2. [Google Colab](#2-google-colab)
3. [Heroku](#3-heroku)
4. [AWS EC2](#4-aws-ec2)
5. [Google Cloud Run](#5-google-cloud-run)
6. [Docker Deployment](#6-docker-deployment)
7. [RunPod / Vast.ai](#7-runpod--vastai)
8. [Troubleshooting](#troubleshooting)

---

## 1. Streamlit Cloud (Recommended)

**Best for**: Quick deployment, free tier available, automatic updates

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)
- Your code in a GitHub repository

### Step-by-Step

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/rag-chatbot.git
   git push -u origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Click "New app"

3. **Configure Deployment**
   - Select your GitHub repo
   - Set branch to `main`
   - Set main file path to `streamlit_app.py`

4. **Add Secrets**
   - Click "Advanced settings" → "Secrets"
   - Add your API keys:
     ```
     OPENAI_API_KEY = "sk-..."
     HUGGINGFACE_API_KEY = "hf_..."
     ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)
   - App is now live!

### Configuration File
Create `streamlit/secrets.toml` in your repo:
```toml
openai_api_key = "sk-..."
environment = "production"
```

### Performance Tips
- Use lightweight embedding model: `all-MiniLM-L6-v2`
- Limit top_k to 3
- Use session state caching
- Consider vector store persistence

---

## 2. Google Colab

**Best for**: Learning, prototyping, no setup required

### Quick Start
1. Open `colab_setup.ipynb`
2. Run cells in order
3. Click the ngrok URL to access your app

### For Persistent Deployment
```python
# In Colab cell:
from google.colab import drive
drive.mount('/content/drive')

# Save code and vector stores to Google Drive
# This persists between sessions
```

### GPU Acceleration
```python
# Enable GPU in Colab:
# Runtime → Change runtime type → GPU (T4 or A100)

# Check GPU availability:
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

---

## 3. Heroku

**Best for**: $5-50/month, simple deployment, good for hobby projects

### Prerequisites
- Heroku account (https://heroku.com)
- Heroku CLI installed
- Your code in GitHub

### Deployment Steps

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku
   
   # Ubuntu
   curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Add Buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   ```

5. **Create Procfile**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.headless=true
   ```

6. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY="sk-..."
   heroku config:set HUGGINGFACE_API_KEY="hf_..."
   ```

7. **Deploy**
   ```bash
   git push heroku main
   ```

8. **View Logs**
   ```bash
   heroku logs --tail
   ```

### Cost Optimization
- Use free dyno tier (sleeps after 30 mins)
- Use lightweight models
- Cache vector stores

---

## 4. AWS EC2

**Best for**: Production, full control, scalability

### Prerequisites
- AWS account
- EC2 instance (Ubuntu 22.04, t2.medium minimum)
- SSH key pair

### Deployment Steps

1. **Launch EC2 Instance**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t2.medium (1GB RAM minimum)
   - Security group: Allow port 80, 443, 8501

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Update System**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

4. **Install Dependencies**
   ```bash
   sudo apt install -y python3-pip python3-venv git nginx certbot python3-certbot-nginx
   ```

5. **Clone Repository**
   ```bash
   git clone https://github.com/username/rag-chatbot.git
   cd rag-chatbot
   ```

6. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. **Create .env File**
   ```bash
   nano .env
   # Add your configuration
   ```

8. **Install Process Manager (PM2)**
   ```bash
   npm install -g pm2
   pm2 start "streamlit run streamlit_app.py" --name rag-chatbot
   pm2 startup
   pm2 save
   ```

9. **Setup Nginx Reverse Proxy**
   ```bash
   sudo nano /etc/nginx/sites-available/default
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   
   ```bash
   sudo systemctl restart nginx
   ```

10. **Setup SSL Certificate**
    ```bash
    sudo certbot certonly --nginx -d your-domain.com
    ```

11. **Monitor Application**
    ```bash
    pm2 monit
    pm2 logs rag-chatbot
    ```

---

## 5. Google Cloud Run

**Best for**: Serverless, auto-scaling, pay-per-use

### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Docker knowledge

### Deployment Steps

1. **Create Cloud Project**
   ```bash
   gcloud projects create rag-chatbot-project
   gcloud config set project rag-chatbot-project
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable container.googleapis.com
   ```

3. **Authenticate Docker**
   ```bash
   gcloud auth configure-docker gcr.io
   ```

4. **Build Docker Image**
   ```bash
   docker build -t gcr.io/rag-chatbot-project/rag-chatbot .
   ```

5. **Push to Google Container Registry**
   ```bash
   docker push gcr.io/rag-chatbot-project/rag-chatbot
   ```

6. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy rag-chatbot \
     --image gcr.io/rag-chatbot-project/rag-chatbot \
     --platform managed \
     --region us-central1 \
     --memory 2Gi \
     --timeout 3600 \
     --set-env-vars OPENAI_API_KEY=sk-...
   ```

7. **View Service**
   ```bash
   gcloud run services describe rag-chatbot
   ```

### Pricing
- First 2 million requests free
- $0.40 per million requests after
- $0.00000025 per vCPU second

---

## 6. Docker Deployment

**For any platform supporting Docker**

### Build Locally
```bash
# Build image
docker build -t rag-chatbot:latest .

# Run locally
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/vector_store:/app/vector_store \
  rag-chatbot:latest
```

### Docker Compose (Multiple Services)
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - VECTOR_STORE_TYPE=chroma
    volumes:
      - ./chroma_db:/app/chroma_db
      - ./vector_store:/app/vector_store
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  chroma:
    image: ghcr.io/chroma-core/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - ./chroma_data:/chroma_data

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### Run with Docker Compose
```bash
docker-compose up -d
```

---

## 7. RunPod / Vast.ai

**For GPU-intensive workloads**

### RunPod Setup

1. **Create RunPod Account**
   - Go to https://runpod.io
   - Create account and add payment method

2. **Select GPU Machine**
   - Choose: RTX 4090, A100, or H100
   - Select image: `pytorch/pytorch:latest`

3. **Launch Pod**
   - Click "Run Pod"
   - Connect via SSH

4. **Install and Deploy**
   ```bash
   git clone <your-repo>
   cd rag-chatbot
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```

5. **Expose to Internet**
   ```bash
   # Using ngrok
   pip install pyngrok
   python -c "from pyngrok import ngrok; print(ngrok.connect(8501))"
   ```

### Cost
- RTX 4090: ~$0.44/hour
- A100: ~$1.29/hour
- H100: ~$2.50/hour

---

## Troubleshooting

### Issue: "Module not found"
```bash
# Solution: Ensure requirements are installed
pip install -r requirements.txt
```

### Issue: "Out of Memory"
```bash
# Use lighter model
EMBEDDING_MODEL=distiluse-base-multilingual-cased-v2

# Reduce batch size
BATCH_SIZE=16

# Use FAISS instead of Chroma
VECTOR_STORE_TYPE=faiss
```

### Issue: "API Key Error"
```bash
# Check environment variable
echo $OPENAI_API_KEY

# Set if missing
export OPENAI_API_KEY=sk-...
```

### Issue: "Connection Timeout"
```bash
# Increase timeout in code
streamlit run streamlit_app.py --logger.level=debug --client.showErrorDetails=true
```

### Issue: "Cold Start Latency"
```python
# Implement caching
@st.cache_resource
def load_rag_pipeline():
    return RAGPipeline()

pipeline = load_rag_pipeline()
```

---

## Performance Comparison

| Platform | Cost | Speed | Setup | Scaling |
|----------|------|-------|-------|---------|
| Streamlit Cloud | Free | Medium | 5 min | Auto |
| Heroku | $5-50 | Medium | 10 min | Manual |
| AWS EC2 | $5-100 | Fast | 30 min | Manual |
| Google Cloud Run | $0-100 | Fast | 20 min | Auto |
| RunPod | $0.44+/hr | Very Fast | 15 min | Manual |
| Colab | Free | Medium | 5 min | N/A |

---

## Monitoring & Logging

### Application Logs
```bash
# Streamlit Cloud
# View in dashboard

# Heroku
heroku logs --tail

# AWS
# CloudWatch Logs

# Google Cloud Run
gcloud run services describe rag-chatbot --format json | grep "traffic"
```

### Performance Monitoring
```python
import time
import streamlit as st

start = time.time()
response, sources = pipeline.query(question)
duration = time.time() - start

st.metric("Response Time", f"{duration:.2f}s")
```

---

## Next Steps

1. **Add Authentication** (if needed)
   - Streamlit auth: https://docs.streamlit.io/deploy/streamlit-cloud/get-started/deploy-an-app

2. **Scale to Production**
   - Implement caching
   - Use load balancer
   - Set up monitoring

3. **Optimize Costs**
   - Cache embeddings
   - Use batch processing
   - Consider local LLM (Ollama)

4. **Add Features**
   - User accounts
   - Document management
   - Analytics dashboard

---

**Happy deploying! 🚀**
