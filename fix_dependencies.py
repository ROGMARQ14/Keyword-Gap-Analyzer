import subprocess
import sys

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")

def main():
    """Install all required dependencies."""
    packages = [
        "streamlit",
        "pandas",
        "numpy",
        "plotly",
        "openai",
        "anthropic",
        "google-generativeai",
        "python-dotenv",
        "toml",
        "seaborn",
        "matplotlib",
        "scikit-learn"
    ]
    
    print("Installing required dependencies...")
    for package in packages:
        install_package(package)
    
    print("\nAll dependencies installed successfully!")
    print("You can now run: streamlit run app.py")

if __name__ == "__main__":
    main()
