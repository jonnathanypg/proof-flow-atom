# Wrapper script to launch the UDF Audit CLI
# Automates Virtual Environment setup and dependency installation with smart detection

# 1. Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo "❌ Error: python3 could not be found."
    echo "Please install Python 3 manually."
    exit 1
fi

# 2. Check Virtual Environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "✅ Running inside active virtual environment: $VIRTUAL_ENV"
else
    # Only create if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    source venv/bin/activate
fi

# 3. Check Dependencies (Smart Check)
# Tries to import critical libraries. If success, skips pip install.
if python -c "import requests" &>/dev/null; then
    echo "✅ Dependencies already installed."
else
    echo "⬇️  Installing dependencies..."
    pip install -r requirements.txt -q
fi

# 4. Run the Menu
echo "🚀 Launching Audit Menu..."
python audit_menu.py

