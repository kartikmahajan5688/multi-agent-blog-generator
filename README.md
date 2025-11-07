# 🤖 Multi-Agent AI Blog Generator

A production-ready multi-agent system that generates high-quality blog posts using three specialized AI agents:

- **Researcher** 🔍: Gathers information and creates outlines
- **Writer** ✍️: Crafts compelling blog content
- **Reviewer** 👁️: Polishes and optimizes the final post

## 🏗️ Architecture

```
User Request → Researcher Agent → Writer Agent → Reviewer Agent → Final Blog Post
```

Built with:

- **FastAPI**: REST API framework
- **LangChain**: LLM orchestration
- **LangGraph**: Agent workflow management
- **OpenAI GPT-4**: Language model

## 🚀 Quick Start

### 1. Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd multi-agent-blog-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Test the API

```bash
# Using curl
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI in Healthcare",
    "tone": "professional",
    "length": "medium"
  }'

# Or visit the interactive docs at:
# http://localhost:8000/docs
```

## 📦 Deployment Options

### Option 1: Render (Recommended)

1. Create a `render.yaml` file:

```yaml
# render.yaml - For Render deployment
services:
  - type: web
    name: multi-agent-blog-generator
    env: python
    region: oregon
    plan: free
    pythonVersion: 3.12.3 # ✅ Ensures compatible wheels (avoids Rust build)
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PORT
        value: 10000
```

2. Push to GitHub and connect to Render
3. Add `OPENAI_API_KEY` in Render dashboard

### Option 2: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:

```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

3. Deploy:

```bash
vercel --prod
```

### Option 3: Hugging Face Spaces

1. Create new Space on Hugging Face
2. Select "Docker" as Space SDK
3. Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

4. Push your code to the Space repository

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PORT`: Server port (default: 8000)

### Request Parameters

```json
{
  "topic": "Your blog topic",
  "tone": "professional|casual|technical|friendly",
  "length": "short|medium|long"
}
```

### Response Format

```json
{
  "topic": "...",
  "research": "Research findings and outline",
  "draft": "Initial blog draft",
  "final_blog": "Polished final version",
  "status": "success"
}
```

## 📊 API Endpoints

| Endpoint    | Method | Description          |
| ----------- | ------ | -------------------- |
| `/`         | GET    | API information      |
| `/health`   | GET    | Health check         |
| `/generate` | POST   | Generate blog post   |
| `/docs`     | GET    | Interactive API docs |

## 🌐 Frontend Integration

The backend is designed to work seamlessly with the companion frontend:
👉 [Multi-Agent Blog Generator Frontend](https://github.com/kartikmahajan5688/ai-blog-generator-frontend)

- The frontend automatically switches between local and production API URLs.
- By default, it expects:
  - **Local:** `http://localhost:8000/generate`
  - **Production:** `https://multi-agent-blog-generator-vugo.onrender.com/generate`

Make sure CORS is enabled in `FastAPI`:

- python
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], # or restrict to your frontend domain
  allow_methods=["*"],
  allow_headers=["*"],
  )

## 🎯 Features

- ✅ Three-stage agent pipeline
- ✅ Customizable tone and length
- ✅ SEO-optimized content
- ✅ Fast response times
- ✅ Error handling and validation
- ✅ OpenAPI documentation
- ✅ CORS enabled for frontend integration

## 💡 Usage Examples

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "Sustainable Tech Innovations",
        "tone": "professional",
        "length": "medium"
    }
)

blog = response.json()
print(blog['final_blog'])
```

### JavaScript

```javascript
const response = await fetch("http://localhost:8000/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    topic: "AI Ethics in 2025",
    tone: "technical",
    length: "long",
  }),
});

const blog = await response.json();
console.log(blog.final_blog);
```

## 🔐 Security Notes

- Never commit your `OPENAI_API_KEY`
- Use environment variables for secrets
- Consider rate limiting for production
- Add authentication if exposing publicly

## 📈 Scaling Tips

1. **Caching**: Add Redis for repeated topics
2. **Async**: Use `asyncio` for parallel agent execution
3. **Queue**: Add Celery for background processing
4. **Monitoring**: Integrate Sentry or similar
5. **Database**: Store generated blogs in PostgreSQL

## 🤝 Contributing

Contributions welcome! Feel free to:

- Add new agent types
- Improve prompts
- Add more customization options
- Enhance error handling

## 📄 License

MIT License - feel free to use in your projects!

## 🆘 Troubleshooting

**Issue**: `OPENAI_API_KEY not found`

- **Solution**: Set the environment variable before running

**Issue**: Slow response times

- **Solution**: Consider using `gpt-3.5-turbo` or caching

**Issue**: Import errors

- **Solution**: Ensure all dependencies are installed with correct versions

---

Built with ❤️ using FastAPI, LangChain, and LangGraph
