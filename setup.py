#!/usr/bin/env python3
"""
Keyword Gap Analyzer - Setup Script
This script helps you get started with the keyword gap analyzer quickly.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print("✅ Python version check passed")
    return True

def install_requirements():
    """Install required packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_secrets_file():
    """Create .streamlit/secrets.toml if it doesn't exist."""
    secrets_path = ".streamlit/secrets.toml"
    if not os.path.exists(".streamlit"):
        os.makedirs(".streamlit")
    
    if not os.path.exists(secrets_path):
        with open(secrets_path, "w") as f:
            f.write("""[api_keys]
# Add your API keys here (optional)
# openai_api_key = "your-openai-key-here"
# anthropic_api_key = "your-anthropic-key-here"
# gemini_api_key = "your-gemini-key-here"
""")
        print("✅ Created .streamlit/secrets.toml template")
    else:
        print("✅ .streamlit/secrets.toml already exists")

def check_streamlit():
    """Check if Streamlit is installed."""
    try:
        import streamlit
        print("✅ Streamlit is installed")
        return True
    except ImportError:
        print("❌ Streamlit not found")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Keyword Gap Analyzer...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Please install dependencies manually: pip install -r requirements.txt")
    
    # Create secrets file
    create_secrets_file()
    
    # Check Streamlit
    if check_streamlit():
        print("\n🎉 Setup complete!")
        print("\nTo start the application:")
        print("  streamlit run app.py")
        print("\nOr use the quick start script:")
        print("  python run.py")
    else:
        print("\n⚠️  Streamlit installation failed. Please install manually:")
        print("  pip install streamlit")

if __name__ == "__main__":
    main()
