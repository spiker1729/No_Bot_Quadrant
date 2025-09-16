#!/bin/bash

# Script to ingest a repository using the Impact Analysis Tool
# Usage: ./scripts/run_ingest.sh <repo_url> [github_token]

set -e

REPO_URL="$1"
GITHUB_TOKEN="$2"
API_URL="http://localhost:8000"

if [ -z "$REPO_URL" ]; then
    echo "❌ Usage: $0 <repo_url> [github_token]"
    echo "   Example: $0 https://github.com/owner/repo"
    echo "   Example: $0 https://github.com/owner/repo ghp_xxxxxxxxxxxx"
    exit 1
fi

echo "🚀 Ingesting repository: $REPO_URL"

# Check if backend is running
if ! curl -s "$API_URL/" > /dev/null 2>&1; then
    echo "❌ Backend is not running. Please start it first:"
    echo "   docker-compose up backend"
    exit 1
fi

# Prepare the request payload
PAYLOAD="{\"repo_url\": \"$REPO_URL\"}"
if [ -n "$GITHUB_TOKEN" ]; then
    PAYLOAD="{\"repo_url\": \"$REPO_URL\", \"github_token\": \"$GITHUB_TOKEN\"}"
fi

echo "📥 Sending ingestion request..."

# Send the request
RESPONSE=$(curl -s -X POST "$API_URL/ingest_repo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

# Check if the request was successful
if echo "$RESPONSE" | grep -q "job_id"; then
    JOB_ID=$(echo "$RESPONSE" | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Ingestion started successfully!"
    echo "📋 Job ID: $JOB_ID"
    echo ""
    echo "🔍 Monitor progress:"
    echo "   docker-compose logs -f backend"
    echo ""
    echo "📊 Check status:"
    echo "   curl -s '$API_URL/jobs/$JOB_ID' | jq"
else
    echo "❌ Ingestion failed:"
    echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
    exit 1
fi
