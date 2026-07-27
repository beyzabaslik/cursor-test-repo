# Company Brain

An enterprise knowledge management and automation platform that leverages AI to manage events, processes, and communications across your organization.

## 🎯 Overview

Company Brain is a comprehensive solution designed to:
- **Ingest** data from multiple sources (Slack, Email, Calendar, etc.)
- **Extract** meaningful events and insights using AI
- **Manage** business processes and automations
- **Analyze** company knowledge using RAG (Retrieval-Augmented Generation)
- **Automate** routine tasks and workflows

## 📁 Project Structure

```
company-brain/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints (chat, ingest, process, automation)
│   │   ├── core/           # Core functionality (LLM, embeddings, config)
│   │   ├── services/       # Business logic services
│   │   ├── pipelines/      # Data processing pipelines
│   │   ├── models/         # Data models
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/               # Frontend application
│   ├── app/
│   ├── components/
│   ├── pages/
│   └── lib/
│
├── contracts/              # API specifications and schemas
│   ├── api_spec.json       # OpenAPI specification
│   └── event_schema.json   # Canonical event schema (frozen — see AGENTS.md)
│
├── data/                   # Data storage
│   ├── raw/               # Raw ingested data
│   └── processed/         # Processed data
│
├── docker/                # Docker configuration
│   ├── Dockerfile         # Backend container
│   └── docker-compose.yml # Multi-container setup
│
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- OpenAI API Key
- Slack Bot Token (optional)
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone the repository**
   ```bash
   cd /Users/pc/Desktop/Company_brain
   ```

2. **Set up environment variables**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies (local development)**
   ```bash
   pip install -r requirements.txt
   ```

4. **Using Docker Compose**
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

### Running the Backend

**Local Development:**
```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 API Endpoints

### Chat API
- `POST /api/chat/message` - Send a chat message
- `WebSocket /api/chat/ws` - Real-time chat connection

### Ingestion API
- `POST /api/ingest/upload` - Upload file for ingestion
- `POST /api/ingest/process` - Process ingested data

### Process API
- `POST /api/process/start` - Start a processing job
- `GET /api/process/status/{process_id}` - Get job status

### Automation API
- `POST /api/automation/trigger` - Trigger an automation
- `GET /api/automation/list` - List all automations

### Cursor Bridge API
- `GET /api/cursor-bridge/health` - Local bridge health check
- `GET /api/cursor-bridge/status` - Provider connection status
- `GET /api/cursor-bridge/tools` - List MCP tools
- `POST /api/cursor-bridge/tools/call` - Invoke an MCP tool
- `GET /api/cursor-bridge/v1/models` - OpenAI-compatible model list
- `POST /api/cursor-bridge/v1/chat/completions` - OpenAI-compatible chat endpoint

Demo UI: `http://localhost:8000/demo/` (YC dashboard) · Bridge console: `http://localhost:8000/demo/pages/bridge.html`

## 🔧 Configuration

### Environment Variables
See [backend/.env.example](backend/.env.example) for all available options.

Key variables:
- `OPENAI_API_KEY` - OpenAI API key for LLM operations
- `CURSOR_BRIDGE_BACKEND` - `mock` (default) or `cursor-mcp`
- `CURSOR_BRIDGE_API_KEY` - Client key for `/api/cursor-bridge/v1/*`
- `CURSOR_MCP_COMMAND` / `CURSOR_MCP_ARGS` - Local MCP server launch command
- `DATABASE_URL` - PostgreSQL connection string
- `SLACK_BOT_TOKEN` - Slack bot authentication token
- `SLACK_SIGNING_SECRET` - Slack request signing secret

## 🏗️ Architecture

### Backend Stack
- **Framework**: FastAPI
- **LLM**: OpenAI GPT-4
- **Embeddings**: OpenAI Embeddings
- **Vector Store**: Pinecone
- **Database**: PostgreSQL
- **Cache**: Redis
- **Async**: asyncio, uvicorn

### Canonical event model

All ingested knowledge is stored as **events** matching `contracts/event_schema.json` (`event_id`, `content`, `raw_type`, `event_type`, `timestamp`, plus structured `metadata` with required `source` and optional `channel` / `tags`). Root fields are fixed; metadata is not a general-purpose bag. See [AGENTS.md](AGENTS.md).

### Core Components

1. **API Layer** (`app/api/`) - HTTP endpoints and WebSocket connections
2. **Services** (`app/services/`) - Business logic and external integrations
3. **Pipelines** (`app/pipelines/`) - Data processing workflows
4. **Core** (`app/core/`) - LLM, embeddings, and configuration
5. **Models** (`app/models/`) - Pydantic data models
6. **Providers** (`app/providers/`) - Cursor MCP provider layer
7. **Bridge** (`app/bridge/`) - Local Cursor Bridge service

## 📋 Features

### Data Ingestion
- Multi-source data collection (Slack, Email, Files)
- Automatic data validation and normalization
- Historical data processing

### Event Extraction
- AI-powered event extraction from unstructured data
- Event classification and tagging
- Metadata enrichment

### Knowledge Management
- RAG-based question answering
- Document chunking and embedding
- Semantic search

### Process Management
- Workflow creation and monitoring
- Automation execution
- Status tracking and notifications

### Slack Integration
- Real-time message processing
- Automated responses
- Event notifications

## 🧪 Testing

```bash
# Run tests
cd backend && pytest tests/

# Bridge smoke test
curl -fsS http://127.0.0.1:8000/api/cursor-bridge/health
curl -fsS http://127.0.0.1:8000/api/cursor-bridge/v1/models \
  -H "Authorization: Bearer sk-curbr-local-dev"
```

## 📝 Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document public functions

### Git Workflow
1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push branch: `git push origin feature/your-feature`
4. Create Pull Request

## 🚨 Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

### API Not Starting
- Check Python version (3.11+)
- Verify all dependencies installed
- Check for port conflicts (8000)

### Slack Integration Issues
- Verify SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET
- Check bot permissions in Slack workspace
- Review Slack API logs

## 📄 License

This project is proprietary and confidential.

## 🤝 Support

For issues and questions, please contact the development team.

---

**Last Updated**: 3 June 2026
