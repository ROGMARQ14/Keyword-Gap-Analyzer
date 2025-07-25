# Keyword Gap Analyzer

A comprehensive, enterprise-ready keyword gap analysis tool built with Python and Streamlit. This application provides deep competitive intelligence for SEO strategies, leveraging AI-powered insights to identify opportunities and drive organic visibility improvements.

## 🚀 Features

### Core Analysis
- **Executive Summary**: High-level metrics and market share analysis
- **Quick Wins**: Keywords where small improvements can yield big results
- **Steal Opportunities**: High-value keywords dominated by competitors
- **Defensive Keywords**: Protect your existing rankings
- **Client Wins**: Showcase where you're outperforming competitors

### Advanced Intelligence
- **Content Funnel Analysis**: TOFU, MOFU, BOFU keyword mapping
- **SERP Feature Opportunities**: Featured snippets, local packs, etc.
- **Trending Keywords**: Identify rising opportunities
- **Competitive Landscape**: Visual position comparisons
- **Opportunity Matrix**: Difficulty vs. volume analysis

### AI-Powered Insights
- **Multi-Model Support**: OpenAI, Anthropic Claude, Google Gemini
- **Strategic Recommendations**: Actionable insights for content strategy
- **Priority Scoring**: Data-driven opportunity ranking
- **Resource Allocation**: ROI-focused recommendations

### Export & Reporting
- **Multiple Formats**: CSV, JSON, Excel
- **Executive Reports**: Ready-to-present summaries
- **Detailed Analysis**: Full keyword lists with metrics
- **Customizable Views**: Filter by volume, difficulty, intent

## 📊 Data Requirements

Your CSV files must include these columns:
- `Keyword` - Target keyword
- `Position` - Current ranking position
- `Previous position` - Previous ranking position
- `Search Volume` - Monthly search volume
- `Keyword Difficulty` - SEO difficulty score (0-100)
- `CPC` - Cost per click
- `URL` - Ranking URL
- `Traffic` - Estimated traffic
- `Traffic (%)` - Traffic percentage
- `Traffic Cost` - Traffic value in USD
- `Competition` - Competition level
- `Number of Results` - SERP competition
- `Trends` - Search trend data
- `Timestamp` - Data collection date
- `SERP Features by Keyword` - SERP features present
- `Keyword Intents` - Search intent classification
- `Position Type` - Type of ranking (organic, featured, etc.)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone [repository-url]
cd keyword-gap-analyzer
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure API keys**:
   - Copy `config.toml.example` to `config.toml`
   - Add your API keys:
```toml
[api_keys]
openai_api_key = "your-openai-key"
anthropic_api_key = "your-anthropic-key"
gemini_api_key = "your-gemini-key"
```

4. **Run the application**:
```bash
streamlit run app.py
```

## 🎯 Usage Guide

### 1. Upload Data
- Upload client CSV file
- Upload competitor CSV file
- Files are validated automatically

### 2. Configure Analysis
- Set minimum search volume threshold
- Adjust maximum keyword difficulty
- Select AI model for insights

### 3. Explore Results
- **Overview Tab**: Competitive landscape visualization
- **Opportunities Tab**: Strategic keyword targets
- **Wins Tab**: Client performance highlights
- **Trends Tab**: Content gap analysis
- **AI Insights Tab**: AI-powered recommendations

### 4. Export Results
- Download individual opportunity lists
- Export full analysis as JSON
- Generate Excel reports
- Save AI insights as text

## 🔍 Analysis Framework

### Opportunity Categories

#### Quick Wins
- Client ranks 6-10, competitor ranks 1-5
- High search volume (>100)
- Low-medium difficulty (<70)

#### Steal Opportunities
- Client ranks 11+ or not ranking
- Competitor ranks 1-5
- High traffic potential

#### Defensive Keywords
- Client ranks 1-5
- Competitor close behind (positions 2-10)
- High value keywords

### Content Funnel Mapping
- **TOFU (Awareness)**: Informational keywords
- **MOFU (Consideration)**: Commercial keywords
- **BOFU (Decision)**: Transactional keywords

### Priority Scoring
```
Priority Score = (Search Volume × 0.4) + 
                 (Traffic Cost × 0.3) + 
                 ((100 - Difficulty) × 0.3)
```

## 🤖 AI Integration

### Supported Models
- **OpenAI GPT-4**: Best for strategic insights
- **Anthropic Claude**: Excellent for content recommendations
- **Google Gemini**: Good for trend analysis

### AI Capabilities
- Strategic content recommendations
- Competitive gap analysis
- Resource allocation guidance
- ROI projections
- Timeline recommendations

## 📈 Example Workflow

1. **Upload Data**: Client and competitor CSV files
2. **Review Summary**: Check executive metrics
3. **Identify Opportunities**: Focus on quick wins and steals
4. **Analyze Content Gaps**: Map keywords to funnel stages
5. **Generate AI Insights**: Get strategic recommendations
6. **Export Results**: Create client-ready reports

## 🔧 Customization

### Configuration Options
- Adjust volume and difficulty thresholds
- Customize scoring weights
- Modify chart colors and styles
- Set export preferences

### Extending the Tool
- Add new analysis metrics
- Integrate additional data sources
- Create custom visualizations
- Implement new AI models

## 📊 Sample Data Format

```csv
Keyword,Position,Previous position,Search Volume,Keyword Difficulty,CPC,URL,Traffic,Traffic (%),Traffic Cost,Competition,Number of Results,Trends,Timestamp,SERP Features by Keyword,Keyword Intents,Position Type
"best seo tools",3,5,18100,65,12.50,https://example.com/seo-tools,5420,15.2,67750,0.89,45600000,0.15,2024-01-15,"Featured snippet,People also ask","Commercial","Organic"
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
- **Streamlit Cloud**: One-click deployment
- **Docker**: Containerized deployment
- **AWS/GCP**: Cloud platform deployment

### Docker Setup
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📝 Support & Contributing

### Issues & Questions
- Check the troubleshooting guide
- Review example data format
- Test with sample datasets

### Contributing
- Fork the repository
- Create feature branches
- Submit pull requests
- Follow coding standards

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Roadmap

- [ ] Real-time SERP monitoring
- [ ] Historical trend analysis
- [ ] Multi-competitor analysis
- [ ] API integration for live data
- [ ] Advanced filtering options
- [ ] White-label reporting
- [ ] Team collaboration features
- [ ] Automated alerts
- [ ] Integration with SEO tools
- [ ] Performance tracking

---

**Built with ❤️ for SEO professionals who demand actionable insights**
