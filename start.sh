#!/bin/bash

# Configuration
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}Starting Terraform Bible Platform...${NC}"

# Check for docker-compose or docker compose
if command -v docker-compose &> /dev/null; then
    DOCKER_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_CMD="docker compose"
else
    echo -e "${RED}[ERROR] Neither 'docker-compose' nor 'docker compose' found in PATH. Please install Docker.${NC}"
    exit 1
fi

$DOCKER_CMD up --build -d

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}[SUCCESS] Platform is successfully running at http://localhost:8000${NC}"
    echo -e "${YELLOW}To stop the platform, run: $DOCKER_CMD down${NC}"
else
    echo -e "\n${RED}[ERROR] Failed to start Docker containers. Please check Docker logs.${NC}"
fi
