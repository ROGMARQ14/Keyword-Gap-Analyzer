from setuptools import setup, find_packages

setup(
    name="keyword-gap-analyzer",
    version="1.0.0",
    description="Enterprise-ready keyword gap analysis tool for SEO competitive intelligence",
    author="SEO Intelligence Team",
    author_email="team@seo-intelligence.com",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.37.0",
        "pandas>=2.2.2",
        "numpy>=1.26.4",
        "plotly>=5.22.0",
        "openai>=1.35.13",
        "anthropic>=0.31.2",
        "google-generativeai>=0.7.2",
        "python-dotenv>=1.0.1",
        "toml>=0.10.2",
        "seaborn>=0.13.2",
        "matplotlib>=3.9.1",
        "scikit-learn>=1.5.1",
        "openpyxl>=3.1.2"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
