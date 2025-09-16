#!/bin/bash

# Initialize the Impact Analysis Tool demo
set -e

echo "🚀 Initializing Impact Analysis Tool Demo"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the demo"
    echo "   Required: EMBEDDING_API_KEY, OPENAI_API_KEY"
    echo "   Optional: GITHUB_TOKEN (for private repos)"
    exit 1
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/{repos,chunks,cache}

# Start the services
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d neo4j qdrant

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check Neo4j
echo "🔍 Checking Neo4j..."
until docker-compose exec neo4j cypher-shell -u neo4j -p password "RETURN 1" > /dev/null 2>&1; do
    echo "   Waiting for Neo4j..."
    sleep 2
done
echo "✅ Neo4j is ready"

# Check Qdrant
echo "🔍 Checking Qdrant..."
until curl -s http://localhost:6333/collections > /dev/null 2>&1; do
    echo "   Waiting for Qdrant..."
    sleep 2
done
echo "✅ Qdrant is ready"

# Start backend
echo "🚀 Starting backend..."
docker-compose up -d backend

# Wait for backend
echo "⏳ Waiting for backend..."
until curl -s http://localhost:8000/ > /dev/null 2>&1; do
    echo "   Waiting for backend..."
    sleep 2
done
echo "✅ Backend is ready"

# Start frontend
echo "🎨 Starting frontend..."
docker-compose up -d frontend

echo ""
echo "✅ Demo initialization complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Neo4j Browser: http://localhost:7474"
echo "   Qdrant Dashboard: http://localhost:6333/dashboard"
echo ""
echo "🧪 Run the demo script:"
echo "   python demo/run_demo.py"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
