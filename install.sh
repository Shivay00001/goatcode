#!/bin/bash

# GOATCODE Installation Script
# This script sets up GOATCODE with all dependencies

set -e

echo "🐐 GOATCODE Installation Script"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo -e "${RED}❌ Python 3.9+ is required (found $python_version)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $python_version found${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 found${NC}"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for Ollama
echo ""
echo "Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
    
    # Check if any models are available
    models=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
    if [ "$models" -eq 0 ]; then
        echo -e "${YELLOW}⚠️  No models found${NC}"
        echo "Would you like to pull a model? (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo "Available models:"
            echo "1. llama2 (general purpose)"
            echo "2. codellama (optimized for code)"
            echo "3. mistral (balanced performance)"
            echo "4. mixtral (high performance)"
            echo ""
            read -p "Enter model number (1-4): " model_choice
            
            case $model_choice in
                1) ollama pull llama2 ;;
                2) ollama pull codellama ;;
                3) ollama pull mistral ;;
                4) ollama pull mixtral ;;
                *) echo "Invalid choice" ;;
            esac
        fi
    else
        echo -e "${GREEN}✅ Found $models model(s)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found${NC}"
    echo "Install from: https://ollama.com"
fi

# Create .env file
echo ""
echo "Setting up configuration..."
if [ ! -f .env ]; then
    cat > .env << EOF
# GOATCODE Configuration
# Uncomment and set values as needed

# OpenAI (optional)
# OPENAI_API_KEY=your-key-here

# Anthropic (optional)
# ANTHROPIC_API_KEY=your-key-here

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434

# Default Provider (ollama, openai, anthropic)
DEFAULT_PROVIDER=ollama
DEFAULT_MODEL=llama2
EOF
    echo -e "${GREEN}✅ Created .env file${NC}"
fi

# Make CLI executable
echo ""
echo "Setting up CLI..."
chmod +x cli/main.py

# Create symlink for global access (optional)
echo ""
read -p "Create global 'goatcode' command? (requires sudo) [y/N]: " global_install
if [[ "$global_install" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    sudo ln -sf "$(pwd)/cli/main.py" /usr/local/bin/goatcode
    echo -e "${GREEN}✅ Created global command 'goatcode'${NC}"
fi

echo ""
echo "================================"
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Quick Start:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start Ollama server: ollama serve"
echo "  3. Run GOATCODE: python -m goatcode --provider ollama"
echo ""
echo "Or use the installed CLI:"
echo "  goatcode --help"
echo ""
echo "Documentation: README.md"
echo "================================"
