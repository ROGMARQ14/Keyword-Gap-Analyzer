# Keyword Gap Analyzer

A comprehensive, enterprise-ready keyword gap analysis tool built with Python and Streamlit. This application provides deep competitive intelligence for SEO strategies, leveraging AI-powered insights to identify opportunities and drive organic visibility improvements.

## 🚀 Features

### Core Analysis
- **Executive Dashboard**: Real-time competitive metrics and market share analysis
- **Quick Wins Identification**: Keywords where you rank 6-10 and competitor ranks 1-5
- **Steal Opportunities**: High-value keywords where competitor ranks 1-5 and you're absent
- **Defensive Keywords**: Keywords to protect where you're ranking well
- **Client Wins**: Keywords where you outperform your competitor

### AI-Powered Insights
- **OpenAI GPT-4 Integration**: Advanced strategic recommendations
- **Anthropic Claude Support**: Alternative AI model for insights
- **Google Gemini**: Latest AI model support
- **Customizable Prompts**: Tailored analysis based on your data

### Advanced Analytics
- **Content Funnel Analysis**: TOFU, MOFU, BOFU keyword categorization
- **SERP Feature Opportunities**: Featured snippets, local packs, people also ask
- **Trending Keywords**: Identifying rising opportunities
- **Traffic Value Analysis**: ROI projections and cost estimates

### Export Capabilities
- **CSV Export**: Raw data for further analysis
- **Excel Reports**: Multi-sheet workbooks with formatting
- **JSON API**: Structured data for integrations
- **AI Insights**: Downloadable strategic recommendations

## 📊 Data Requirements

### Required Columns
Your CSV/Excel files must contain these columns:

| Column | Description |
|--------|-------------|
| Keyword | Search term |
| Position | Current ranking position |
| Previous position | Previous ranking position |
| Search Volume | Monthly search volume |
| Keyword Difficulty | SEO difficulty score (0-100) |
| CPC | Cost per click |
| URL | Ranking URL |
| Traffic | Estimated traffic |
| Traffic (%) | Traffic percentage |
| Traffic Cost | Traffic value in USD |
| Competition | Competition level |
| Number of Results | Total results |
| Trends | Trend indicator |
| Timestamp | Data collection date |
| SERP Features by Keyword | SERP features present |
| Keyword Intents | Search intent |
| Position Type | Type of position |

## 🛠️ Installation

### Quick Start (Windows)
1. Download the project
2. Run `install.bat` to set up the environment
3. Run `run.bat` to start the application
4. Open http://localhost:8501 in your browser

### Manual Installation
```bash
# Clone the repository
git clone <repository-url>
cd keyword-gap-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys (optional)
# Edit config.toml with your API keys

# Run the application
streamlit run app.py
```

## 🔧 Configuration

### API Keys Setup
Create a `config.toml` file in the project root:

```toml
[api_keys]
openai_api_key = "your-openai-key"
anthropic_api_key = "your-anthropic-key"
gemini_api_key = "your-gemini-key"

[analysis]
default_model = "openai"
confidence_threshold = 0.8
min_search_volume = 100
max_keyword_difficulty = 70

[strategy]
quick_win_threshold = 10
defensive_threshold = 5
long_term_threshold = 50
```

### Streamlit Secrets
Alternatively, add API keys to Streamlit secrets:
```toml
[api_keys]
openai_api_key = "your-openai-key"
anthropic_api_key = "your-anthropic-key"
gemini_api_key = "your-gemini-key"
```

## 📈 Usage Guide

### 1. Upload Data
- Upload client CSV/Excel file
- Upload competitor CSV/Excel file
- Enter custom names for easy identification

### 2. Configure Settings
- Set minimum search volume threshold
- Adjust maximum keyword difficulty
- Select AI model for insights

### 3. Analyze Results
- **Overview Tab**: High-level performance metrics
- **Opportunities Tab**: Strategic keyword opportunities
- **Wins Tab**: Keywords where you outperform competitor
- **AI Insights Tab**: AI-generated strategic recommendations

### 4. Export Data
- Download opportunities as CSV
- Export full analysis as JSON
- Generate Excel reports with multiple sheets

## 🎯 Strategic Framework

### Quick Wins (30-day actions)
- Keywords ranking 6-10 vs competitor 1-5
- Low difficulty, high volume opportunities
- Existing content optimization potential

### Steal Opportunities (3-month strategy)
- Competitor ranks 1-5, you're absent
- High traffic value keywords
- Content gap identification

### Defensive Keywords (Ongoing)
- You rank 1-5, competitor close behind
- High-value keywords to protect
- Monitor for ranking drops

### Long-term Investment (6-12 months)
- High difficulty, high value keywords
- Brand building opportunities
- Authority development targets

## 🎨 Customization

### Adding New Metrics
Extend the analyzer in `core/analyzer.py`:
```python
def get_custom_metric(self):
    # Your custom analysis logic
    return pd.DataFrame()
```

### Custom AI Prompts
Modify prompts in `utils/ai_analyzer.py`:
```python
def _build_analysis_prompt(self, data):
    # Customize AI analysis prompts
    return custom_prompt
```

### New Visualizations
Add charts in `visualization/charts.py`:
```python
@staticmethod
def create_custom_chart(data):
    # Your custom visualization
    return fig
```

## 📋 Sample Data
Sample CSV files are provided in the `examples/` directory:
- `sample_client_data.csv`: Example client keyword data
- `sample_competitor_data.csv`: Example competitor keyword data

## 🔍 Troubleshooting

### Common Issues

**Import Error**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

**API Key Error**: Check config.toml or Streamlit secrets
- Verify API keys are correctly formatted
- Ensure keys have proper permissions

**Data Format Error**: Verify CSV columns match requirements
- Check for missing required columns
- Ensure numeric columns contain valid numbers

### Performance Optimization
- Use CSV files under 100MB for best performance
- Filter data before upload for faster processing
- Adjust Streamlit settings for large datasets

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License
MIT License - see LICENSE file for details

## 🆘 Support
- Create an issue on GitHub
- Check the troubleshooting section
- Review sample data for format guidance

## 🔄 Updates
Stay updated with the latest features:
- Follow the repository
- Check release notes
- Update dependencies regularly
