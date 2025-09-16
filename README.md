# Impact Analysis Tool

A sophisticated code analysis platform that helps developers understand the ripple effects of code changes in large repositories. The tool combines repository ingestion, intelligent graph analysis, interactive visualizations, and AI-powered Q&A capabilities to provide comprehensive insights into code dependencies and potential impacts.

## 🚀 Features

### Core Capabilities
- **Repository Ingestion**: Clone and analyze public GitHub repositories
- **Interactive Graph Visualizations**: Multiple layout algorithms including spider web, force-directed, and tree layouts
- **Code Dependency Analysis**: Understand relationships between files, functions, and classes
- **Diff Impact Analysis**: Analyze the potential impact of code changes (expandable)
- **AI-Powered Q&A**: Ask questions about your codebase with context-aware responses
- **Multi-Language Support**: Python, TypeScript, JavaScript, Java, Go, Rust, C++

### Visualization Features
- **Spider Web Layout**: Advanced fcose algorithm for complex dependency visualization
- **Force-Directed Layout**: Cola algorithm for natural clustering
- **Tree Layout**: Hierarchical breadthfirst for repository structure
- **Interactive Controls**: Zoom, pan, fit, and layout switching
- **Node Highlighting**: Hover effects and selection states
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

### Backend (Python FastAPI)
- **API Layer**: RESTful endpoints with FastAPI and automatic OpenAPI documentation
- **Graph Database**: Neo4j for storing and querying code relationships
- **Vector Database**: Qdrant for semantic search and embeddings
- **AST Processing**: Tree-sitter for multi-language code parsing
- **Repository Management**: GitPython for cloning and git operations

### Frontend (React TypeScript)
- **UI Framework**: React 18 with TypeScript for type safety
- **Styling**: Tailwind CSS for responsive design
- **Graph Visualization**: Cytoscape.js with advanced layout algorithms
- **Build Tool**: Vite for fast development and optimized builds
- **State Management**: React hooks for local state management

### Infrastructure
- **Containerization**: Docker and Docker Compose for easy deployment
- **Development**: Hot reload for both frontend and backend
- **Databases**: Containerized Neo4j and Qdrant instances

## 🛠️ Tech Stack

### Backend Dependencies
- **Core**: FastAPI, Uvicorn, Pydantic v2
- **Databases**: Neo4j driver, Qdrant client
- **Code Analysis**: Tree-sitter parsers for multiple languages
- **Git Operations**: GitPython
- **AI/ML**: OpenAI API, tiktoken for tokenization
- **Utilities**: httpx, orjson, tenacity, python-multipart

### Frontend Dependencies
- **Core**: React 18, TypeScript, Vite
- **Visualization**: Cytoscape.js with fcose, cola, and cose-bilkent layouts
- **Styling**: Tailwind CSS, clsx, tailwind-merge
- **Icons**: Lucide React
- **HTTP**: Axios for API communication

## 📋 Prerequisites

- **Python**: 3.10+ (recommended: 3.11 or 3.12)
- **Node.js**: 18+ (recommended: 18.17+ or 20+)
- **Git**: Latest version
- **Docker**: Latest Docker Desktop (for containerized setup)
- **Memory**: 4GB+ RAM recommended for large repositories

## 🚀 Setup Instructions

### Option 1: Local Development (Recommended)

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd impact-analysis-tool
```

#### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start backend server
cd backend
python -m uvicorn src.impact_analysis.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

#### 3. Frontend Setup
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at:
- **Application**: http://localhost:3001 (or the port shown in terminal)

### Option 2: Docker Compose (Full Stack)

#### 1. Start All Services
```bash
# From project root
docker compose up -d --build
```

#### 2. Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474
- **Qdrant Dashboard**: http://localhost:6333/dashboard

#### 3. Stop Services
```bash
docker compose down
```

## 🎯 Usage Guide

### 1. Repository Ingestion
1. Navigate to the **Ingest Repo** tab
2. Enter a GitHub repository URL in any of these formats:
   - `https://github.com/owner/repo`
   - `github.com/owner/repo`
   - `owner/repo`
3. Click **Ingest Repository**
4. Wait for processing to complete (progress shown in UI)

### 2. Graph Visualization
#### Code Graph Visualization
1. Go to **View Graph** tab
2. Select a node (file, function, or class) from the list
3. Click **Load Graph** to see its dependency network
4. Use layout buttons to switch between:
   - **Spider Web**: Advanced force-directed layout for complex relationships
   - **Force**: Cola algorithm for natural clustering
   - **Circle**: Circular arrangement
   - **Organic**: Cose algorithm for organic layouts

#### Full Repository Graph
1. Go to **Full Graph** tab
2. View the complete repository structure
3. Switch between layout algorithms
4. Use **Fit** button to center and scale the graph

### 3. Interactive Features
- **Zoom**: Mouse wheel or pinch gestures
- **Pan**: Click and drag empty space
- **Select Nodes**: Click on nodes to highlight
- **Hover Effects**: Hover over nodes for visual feedback
- **Layout Controls**: Use buttons to change visualization style

### 4. Ask Questions
1. Navigate to **Ask Questions** tab
2. Type your question about the codebase
3. Get AI-powered responses with code context

### 5. Diff Analysis
1. Go to **Analyze Diff** tab
2. Paste your git diff or code changes
3. Get impact analysis (feature under development)

## 🔌 API Reference

### Repository Ingestion
```bash
POST /api/ingest_repo
Content-Type: application/json

{
  "repo_url": "https://github.com/django/django"
}
```

### Graph Operations
```bash
# Get node graph
GET /api/graph/{node_id}

# List available nodes
POST /api/graph/list_nodes
{
  "repo_path": "/path/to/repo"
}

# Get full repository tree
POST /api/graph/repo_tree
{
  "repo_path": "/path/to/repo",
  "max_nodes": 800
}

# Get full graph with relationships
POST /api/graph/full
{
  "repo_path": "/path/to/repo"
}
```

### Analysis Operations
```bash
# Analyze diff impact
POST /api/analyze_diff
{
  "repo_path": "/path/to/repo",
  "diff_text": "git diff content"
}

# Ask questions
POST /api/ask
{
  "question": "How does authentication work?",
  "repo_path": "/path/to/repo",
  "context_ids": ["optional", "context", "files"]
}
```

## 🧪 Demo and Testing

### Run Demo Script
```bash
# Activate virtual environment
source venv/bin/activate

# Run comprehensive demo
python demo/run_demo.py
```

### Manual Testing
1. **Sample Repository**: Try with `octocat/Hello-World` for quick testing
2. **Large Repository**: Test with `django/django` for comprehensive analysis
3. **Multi-language**: Test with repositories containing multiple programming languages

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
# API Configuration
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=http://localhost:6333
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Development
DEBUG=true
LOG_LEVEL=info
```

### Database Configuration
- **Neo4j**: Configured in `infra/neo4j/neo4j.conf`
- **Qdrant**: Configured in `infra/qdrant/config.yaml`

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
- **404 errors**: Ensure API endpoints use `/api/` prefix
- **Python not found**: Activate virtual environment with `source venv/bin/activate`
- **Import errors**: Verify all dependencies are installed with `pip install -r backend/requirements.txt`

#### Frontend Issues
- **Port conflicts**: Frontend auto-selects available ports (3001, 3002, etc.)
- **Build errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- **Graph not rendering**: Check browser console for JavaScript errors

#### Docker Issues
- **Port conflicts**: Ensure ports 3000, 6333, 7474, 7687, 8000 are available
- **Container issues**: Rebuild with `docker compose up --build --force-recreate`
- **Memory issues**: Increase Docker memory allocation

#### Graph Visualization Issues
- **Nodes not visible**: Use **Fit** button to center the graph
- **Performance issues**: Reduce `max_nodes` parameter for large repositories
- **Layout problems**: Try different layout algorithms using the control buttons

### Performance Optimization
- **Large Repositories**: Increase `max_nodes` limit gradually
- **Memory Usage**: Monitor RAM usage with large graphs
- **Network**: Ensure stable internet for repository cloning

## 🚧 Development

### Backend Development
```bash
# Install development dependencies
pip install -r backend/requirements.txt

# Run tests
cd backend
python -m pytest

# Code formatting
black src/
isort src/

# Type checking
mypy src/
```

### Frontend Development
```bash
# Install dependencies
npm install

# Development server with hot reload
npm run dev

# Type checking
npm run build

# Linting
npm run lint
```

### Adding New Features
1. **Backend**: Add routes in `src/impact_analysis/api/`
2. **Frontend**: Add components in `src/components/`
3. **Graph Layouts**: Extend cytoscape configurations
4. **Language Support**: Add tree-sitter parsers

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed description
4. Include logs and system information

---

**Built with ❤️ for developers who need to understand code impact**
