# Modal Deployment Guide - Blogger Agent TFG

**Complete guide for deploying the Blogger Agent backend on Modal serverless platform.**

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Modal Setup](#modal-setup)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Testing](#testing)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)
- [Future: HuggingFace Models](#future-huggingface-models)

---

## 🎯 Prerequisites

### 1. Install Modal CLI

```bash
pip install modal
```

### 2. Create Modal Account

Visit [modal.com](https://modal.com) and sign up for a free account.

### 3. Authenticate

```bash
modal token new
```

This will open a browser window to authenticate with Modal.

### 4. Verify Installation

```bash
modal --version
```

---

## 🔧 Modal Setup

### 1. Configure OpenAI Secret

Modal uses "secrets" to securely store API keys. Create your OpenAI secret:

```bash
modal secret create openai-secret OPENAI_API_KEY="sk-your-actual-api-key-here"
```

**Important:** Replace `sk-your-actual-api-key-here` with your real OpenAI API key.

To verify your secret:

```bash
modal secret list
```

You should see `openai-secret` in the list.

### 2. Update Secret (if needed)

If you need to update your API key later:

```bash
modal secret delete openai-secret
modal secret create openai-secret OPENAI_API_KEY="sk-new-key"
```

---

## 📦 Configuration

The deployment configuration is in `backend/modal_app.py`. Key settings:

### Resource Allocation

```python
@app.function(
    image=image,
    secrets=[modal.Secret.from_name("openai-secret")],
    timeout=600,      # 10 minutes max execution time
    memory=2048,      # 2GB RAM
)
```

### Docker Image

The app uses a Debian Slim image with Python 3.11 and installs dependencies from `requirements.txt`:

```python
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("requirements.txt")
    .apt_install("git")
)
```

---

## 🚀 Deployment

### 1. Local Testing (Optional but Recommended)

Test the app locally before deploying:

```bash
cd backend
python modal_app.py
```

This runs the orchestrator locally with mock data to verify everything works.

### 2. Deploy to Modal

From the project root:

```bash
modal deploy backend/modal_app.py
```

**Expected Output:**
```
✓ Created objects.
├── 🔨 Created mount /code
├── 🔨 Created function generate_blog_post.
├── 🔨 Created function scrape_blogger_corpus.
└── 🔨 Created web endpoint webhook.

✓ App deployed! 🎉

View your endpoints:
https://[your-username]--blogger-agent-tfg-webhook.modal.run
```

**Save your webhook URL!** You'll need it to make API calls.

### 3. View Deployment Status

```bash
modal app list
```

---

## 🧪 Testing

### Test the Webhook

#### Using cURL:

```bash
curl -X POST https://[your-username]--blogger-agent-tfg-webhook.modal.run \
  -H "Content-Type: application/json" \
  -d '{
    "blogger_urls": [
      "https://javipas.com/post1",
      "https://javipas.com/post2"
    ],
    "topic": "Las mejores prácticas para desarrollar APIs REST con Python",
    "enable_critique": true,
    "min_word_count": 800,
    "max_word_count": 2500
  }'
```

#### Using Python:

```python
import requests

url = "https://[your-username]--blogger-agent-tfg-webhook.modal.run"
payload = {
    "blogger_urls": [
        "https://javipas.com/post1",
        "https://javipas.com/post2"
    ],
    "topic": "Las mejores prácticas para desarrollar APIs REST con Python",
    "enable_critique": True,
    "min_word_count": 800,
    "max_word_count": 2500
}

response = requests.post(url, json=payload)
result = response.json()

if result["success"]:
    print(f"Generated post with {len(result['data']['content'])} characters")
    print(f"HTML Length: {len(result['data']['html_structure']['html'])}")
else:
    print(f"Error: {result['error']}")
```

#### Using JavaScript (Next.js):

```typescript
// app/api/generate-post/route.ts
export async function POST(request: Request) {
  const { bloggerUrls, topic } = await request.json();
  
  const response = await fetch(
    "https://[your-username]--blogger-agent-tfg-webhook.modal.run",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        blogger_urls: bloggerUrls,
        topic: topic,
        enable_critique: true,
      }),
    }
  );
  
  const result = await response.json();
  
  if (result.success) {
    return Response.json(result.data);
  } else {
    return Response.json({ error: result.error }, { status: 500 });
  }
}
```

### Expected Response Format

```json
{
  "success": true,
  "data": {
    "workflow_id": "abc123",
    "topic": "Las mejores prácticas para desarrollar APIs REST con Python",
    "blogger_urls": ["..."],
    "style_profile": {
      "tone": "conversational, humorous, personal",
      "voice": "first person",
      ...
    },
    "keywords": ["api", "rest", "python", ...],
    "content": "# Post Title\n\nContent here...",
    "html_structure": {
      "html": "<article>...</article>",
      "jsx": "<article className=\"blog-post\">...</article>",
      "metadata": {
        "title": "Post Title",
        "description": "Description...",
        "keywords": ["..."],
        "reading_time": 5,
        "word_count": 1234,
        "slug": "post-title"
      },
      "headings": [...],
      "nextjs_component": "import React..."
    },
    "image_prompts": [
      {
        "position": "header",
        "prompt": "Professional hero image...",
        "alt_text": "..."
      }
    ],
    "metadata": {
      "duration": 1.5,
      "phases": {...}
    }
  },
  "error": null
}
```

---

## 📊 Usage

### Typical Workflow

1. **Frontend** sends request with blogger URLs and topic
2. **Modal** executes the orchestrator serverlessly
3. **Orchestrator** runs all 7 phases:
   - Style Analysis
   - Keyword Extraction
   - Content Generation
   - Critique
   - Refinement (if needed)
   - HTML Building
   - Image Selection
4. **Response** includes complete blog post data
5. **Frontend** displays the generated post

### Execution Time

Typical execution: **30-60 seconds** (depends on OpenAI API response times)

### Cost Estimate

Modal charges for compute time:
- **Free tier:** 30 hours/month
- **Paid:** ~$0.0001/second of CPU execution

With 2GB RAM for 60 seconds:
- **~$0.006 per post generation** (very economical!)
- **Free tier:** ~300,000 post generations/month

---

## 🛠️ Troubleshooting

### Error: "Secret not found: openai-secret"

**Solution:**
```bash
modal secret create openai-secret OPENAI_API_KEY="sk-your-key"
```

### Error: "No module named 'src'"

**Solution:** Make sure you're deploying from the correct directory:
```bash
# From project root:
modal deploy backend/modal_app.py

# NOT from backend/:
cd backend && modal deploy modal_app.py  # ❌ Wrong
```

### Error: "Timeout exceeded"

**Solution:** Increase timeout in `modal_app.py`:
```python
@app.function(
    timeout=900,  # 15 minutes
    ...
)
```

### View Logs

```bash
modal app logs blogger-agent-tfg
```

### Cold Start Issues

First request after deployment may be slow (image building). Subsequent requests are fast.

---

## 💰 Cost Optimization

### 1. Reduce Memory if Possible

```python
@app.function(
    memory=1024,  # Try 1GB instead of 2GB
    ...
)
```

### 2. Optimize OpenAI Calls

- Use `gpt-3.5-turbo` for non-critical phases
- Cache style analysis for repeated blogger analysis
- Batch requests when possible

### 3. Implement Caching

```python
from modal import Dict

# Cache style profiles to avoid re-analyzing same blogger
style_cache = Dict.from_name("style-profiles", create_if_missing=True)

@app.function(...)
def cached_style_analysis(blogger_urls):
    key = "_".join(sorted(blogger_urls))
    if key in style_cache:
        return style_cache[key]
    
    # Analyze and cache
    result = analyze_style(blogger_urls)
    style_cache[key] = result
    return result
```

---

## 🚀 Future: HuggingFace Models

**PLANNED BUT NOT YET IMPLEMENTED**

### Objective

Migrate from OpenAI to open-source HuggingFace models to:
- Reduce costs significantly
- Have more control over inference
- Support offline/local development
- Experiment with different model architectures

### Option 1: HuggingFace Models on Modal GPU

Use open-source models (Llama, Mistral, etc.) directly in Modal:

```python
# Future implementation
image_gpu = (
    modal.Image.debian_slim()
    .pip_install("transformers", "torch", "accelerate")
)

@app.function(
    image=image_gpu,
    gpu="A10G",  # Modal GPU
    timeout=300,
)
def generate_with_llama(prompt: str) -> str:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=2000)
    
    return tokenizer.decode(outputs[0])
```

### Option 2: HuggingFace Inference API

Use HuggingFace's hosted inference:

```python
# Future implementation
@app.function(
    secrets=[modal.Secret.from_name("huggingface-secret")],
)
def generate_with_hf_api(prompt: str) -> str:
    import requests
    
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
    headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.json()[0]["generated_text"]
```

### Hybrid Approach (Recommended for Future)

- **Style Analysis:** GPT-4 (best quality)
- **Content Generation:** Llama/Mistral on Modal GPU (cost-effective)
- **Critique:** GPT-3.5-turbo (balance of quality/cost)
- **HTML/Images:** Rule-based (no LLM needed)

### Resources

- [Modal GPU Documentation](https://modal.com/docs/guide/gpu)
- [HuggingFace Inference API](https://huggingface.co/docs/api-inference/)
- [Transformers Library](https://huggingface.co/docs/transformers/)

---

## 📝 Additional Commands

### Redeploy After Changes

```bash
modal deploy backend/modal_app.py
```

### Run Function Locally (for debugging)

```bash
modal run backend/modal_app.py::generate_blog_post \
  --blogger-urls '["url1", "url2"]' \
  --topic "Test Topic"
```

### Stop/Delete App

```bash
modal app stop blogger-agent-tfg
```

---

## 🔗 Next Steps

1. ✅ Deploy backend to Modal
2. Create Next.js frontend (Issue #4)
3. Connect frontend to Modal webhook
4. Deploy frontend to Vercel
5. End-to-end testing

---

**Last Updated:** February 10, 2026  
**Deployment Status:** Ready for deployment  
**Backend:** ~75% complete
