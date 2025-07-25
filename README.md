# 🔍 Keyword Gap Analyzer

An enterprise-ready Streamlit application for comprehensive keyword gap analysis and competitive intelligence.

## 🚀 Features

### Comprehensive Analysis
- **Executive Summary** - Key metrics and market position
- **Quick Wins** - Keywords where you can quickly improve rankings
- **Steal Opportunities** - High-value keywords to target from competitors
- **Defensive Keywords** - Protect your current rankings
- **Content Gaps** - TOFU/MOFU/BOFU funnel analysis
- **Trending Keywords** - Emerging opportunities

### AI-Powered Insights
- **OpenAI GPT-4** integration
- **Anthropic Claude** support
- **Google Gemini** compatibility
- **Strategic recommendations** based on data

### Interactive Visualizations
- **Position comparison charts**
- **Market share analysis**
- **Opportunity matrices**
- **Funnel gap visualization**
- **Trend analysis**

### Export Capabilities
- **CSV exports** for all analysis types
- **Excel workbooks** with multiple sheets
- **Filtered data downloads**
- **Complete analysis reports**

## 📋 Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- OpenAI API key (optional)
- Anthropic API key (optional)
- Google Gemini API key (optional)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd keyword-gap-analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API keys (optional):**

### Option 1: Using config.toml
Edit `config.toml`:
```toml
[api_keys]
openai_api_key = "your-openai-key"
anthropic_api_key = "your-anthropic-key"
gemini_api_key = "your-gemini-key"
```

### Option 2: Using Streamlit secrets
Create `.streamlit/secrets.toml`:
```toml
[api_keys]
openai_api_key = "your-openai-key"
anthropic_api_key = "your-anthropic-key"
gemini_api_key = "your-gemini-key"
```

## 🎯 Usage

1. **Start the application:**
```bash
streamlit run app.py
```

2. **Upload your data:**
   - Upload client CSV file
   - Upload competitor CSV file

3. **Configure analysis:**
   - Set minimum search volume
   - Set maximum keyword difficulty
   - Select AI model (if configured)

4. **Analyze results:**
   - View executive summary
   - Explore opportunities
   - Generate AI insights
   - Export findings

## 📊 Data Format

Your CSV files should contain these columns:
- `Keyword` - Search term
- `Position` - Current ranking position
- `Previous position` - Previous ranking position
- `Search Volume` - Monthly search volume
- `Keyword Difficulty` - SEO difficulty score (0-100)
- `CPC` - Cost per click
- `URL` - Ranking URL
- `Traffic` - Estimated traffic
- `Traffic (%)` - Traffic percentage
- `Traffic Cost` - Traffic value
- `Competition` - Competition level
- `Number of Results` - SERP results count
- `Trends` - Search trend data
- `Timestamp` - Data collection date
- `SERP Features by Keyword` - SERP features
- `Keyword Intents` - Search intent
- `Position Type` - Type of ranking

## 🔧 Configuration

Edit `config.toml` to customize:
- Default AI model
- Analysis thresholds
- Visualization settings
- Strategy parameters

## 📈 Analysis Framework

### Quick Wins
Keywords where you rank 6-10 and competitor ranks 1-5. These offer immediate optimization opportunities.

### Steal Opportunities
Keywords where competitor ranks 1-5 and you're absent or ranking poorly. High-value targets for new content.

### Defensive Keywords
Keywords where you rank 1-5 but competitor is close. Protect these valuable positions.

### Content Gaps
Missing keywords by funnel stage:
- **TOFU** (Awareness) - Informational content
- **MOFU** (Consideration) - Comparison content
- **BOFU** (Decision) - Commercial content

## 🎨 Customization

### Adding New Metrics
Extend the analyzer in `core/analyzer.py`:

```python
def add_custom_metric(self, df):
    df['Custom Score'] = df['Search Volume'] * df['CPC']
    return df
```

### Custom Visualizations
Add new charts in `visualization/charts.py`:

```python
@staticmethod
def create_custom_chart(data):
    # Your custom visualization
    pass
```

## 🐛 Troubleshooting

### Common Issues

**"Missing required columns" error:**
- Ensure your CSV files contain all required columns
- Check column names match exactly

**"AI model not configured":**
- Add API keys to config.toml or .streamlit/secrets.toml
- Restart the application after configuration

**"No opportunities found":**
- Lower minimum search volume threshold
- Increase maximum keyword difficulty
- Check data quality and completeness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review example data files

## 🏆 Example Use Cases

### E-commerce SEO
- Identify product keyword opportunities
- Analyze competitor product pages
- Optimize category rankings

### SaaS Marketing
- Find software comparison keywords
- Target feature-specific searches
- Build authority in niche topics

### Local Business
- Discover local search opportunities
- Analyze nearby competitors
- Optimize for "near me" searches

### Content Marketing
- Identify content gaps
- Plan editorial calendar
- Prioritize high-impact topics
