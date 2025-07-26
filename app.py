import streamlit as st
import pandas as pd
import json
from utils.data_loader import DataLoader
from core.analyzer import KeywordGapAnalyzer
from utils.ai_analyzer import AIAnalyzer

# Page configuration
st.set_page_config(
    page_title="Keyword Gap Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_analyzer():
    return KeywordGapAnalyzer()

@st.cache_resource
def init_ai_analyzer():
    return AIAnalyzer()

analyzer = init_analyzer()
ai_analyzer = init_ai_analyzer()

# Main header
st.title("🔍 Keyword Gap Analyzer")
st.markdown("### Comprehensive SEO Competitive Intelligence Platform")

# Sidebar
with st.sidebar:
    st.header("📊 Data Upload")
    
    client_name = st.text_input("Client Name", value="Client")
    competitor_name = st.text_input("Competitor Name", value="Competitor")
    
    client_file = st.file_uploader("Upload Client File", type=['csv', 'xlsx', 'xls'])
    competitor_file = st.file_uploader("Upload Competitor File", type=['csv', 'xlsx', 'xls'])
    
    st.header("🤖 AI Analysis")
    available_models = [m for m in ['openai', 'anthropic', 'gemini'] if ai_analyzer.is_configured(m)]
    selected_model = st.selectbox("Select AI Model", available_models) if available_models else None
    
    st.header("⚙️ Settings")
    min_volume = st.slider("Minimum Search Volume", 0, 1000, 100)
    max_difficulty = st.slider("Maximum Keyword Difficulty", 0, 100, 50)

# Main content
if client_file and competitor_file:
    with st.spinner("Loading and validating data..."):
        client_df = DataLoader.load_file(client_file)
        competitor_df = DataLoader.load_file(competitor_file)
    
    if client_df is not None and competitor_df is not None:
        analyzer.load_data(client_df, competitor_df)
        
        # Get analysis results
        quick_wins = analyzer.get_quick_wins()
        steal_ops = analyzer.get_steal_opportunities()
        defensive = analyzer.get_defensive_keywords()
        client_wins = analyzer.get_client_wins()
        summary = analyzer.get_executive_summary()
        
        # Executive Summary
        st.header(f"📈 Executive Summary: {client_name} vs {competitor_name}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{client_name} Keywords", f"{summary['client']['total_keywords']:,}")
            st.metric(f"{client_name} Avg Position", f"{summary['client']['avg_position']:.1f}")
        with col2:
            st.metric(f"{competitor_name} Keywords", f"{summary['competitor']['total_keywords']:,}")
            st.metric(f"{competitor_name} Avg Position", f"{summary['competitor']['avg_position']:.1f}")
        with col3:
            st.metric("Market Share", f"{summary['market_share']['client']:.1f}%")
            st.metric("Opportunity Score", f"{summary['opportunity_score']:,}")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Opportunities", "🏆 Wins", "🤖 AI Insights"])
        
        with tab1:
            st.header("Performance Overview")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"{client_name} Summary")
                st.json({
                    'Total Keywords': summary['client']['total_keywords'],
                    'Average Position': f"{summary['client']['avg_position']:.1f}",
                    'Total Traffic': f"{summary['client']['total_traffic']:,}",
                    'Traffic Cost': f"${summary['client']['total_traffic_cost']:,.2f}"
                })
            with col2:
                st.subheader(f"{competitor_name} Summary")
                st.json({
                    'Total Keywords': summary['competitor']['total_keywords'],
                    'Average Position': f"{summary['competitor']['avg_position']:.1f}",
                    'Total Traffic': f"{summary['competitor']['total_traffic']:,}",
                    'Traffic Cost': f"${summary['competitor']['total_traffic_cost']:,.2f}"
                })
        
        with tab2:
            st.header("Strategic Opportunities")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🚀 Quick Wins")
                if not quick_wins.empty:
                    st.dataframe(quick_wins.head(10))
                else:
                    st.info("No quick wins found")
                
                st.subheader("🛡️ Defensive Keywords")
                if not defensive.empty:
                    st.dataframe(defensive.head(10))
                else:
                    st.info("No defensive keywords found")
            
            with col2:
                st.subheader("🔥 Steal Opportunities")
                if not steal_ops.empty:
                    st.dataframe(steal_ops.head(10))
                else:
                    st.info("No steal opportunities found")
        
        with tab3:
            st.header("Client Wins")
            if not client_wins.empty:
                st.dataframe(client_wins.head(20))
            else:
                st.info("No client wins found")
        
        with tab4:
            st.header("AI Strategic Insights")
            if selected_model and st.button("Generate AI Insights", type="primary"):
                analysis_data = {
                    'client_total_keywords': summary['client']['total_keywords'],
                    'client_avg_position': summary['client']['avg_position'],
                    'client_total_traffic': summary['client']['total_traffic'],
                    'client_traffic_cost': summary['client']['total_traffic_cost'],
                    'competitor_total_keywords': summary['competitor']['total_keywords'],
                    'competitor_avg_position': summary['competitor']['avg_position'],
                    'competitor_total_traffic': summary['competitor']['total_traffic'],
                    'competitor_traffic_cost': summary['competitor']['total_traffic_cost'],
                    'quick_wins': quick_wins.head(10).to_dict('records'),
                    'steal_opportunities': steal_ops.head(10).to_dict('records'),
                    'defensive_keywords': defensive.head(10).to_dict('records')
                }
                
                with st.spinner("Generating AI insights..."):
                    insights = ai_analyzer.generate_insights(analysis_data, selected_model)
                    st.markdown("### 🤖 AI Strategic Recommendations")
                    st.markdown(insights)
                    
                    st.download_button(
                        label="Download AI Insights",
                        data=insights,
                        file_name="ai_strategic_insights.txt",
                        mime="text/plain"
                    )
        
        # Export functionality
        st.header("📥 Export Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            all_opportunities = pd.concat([
                quick_wins.assign(Type='Quick Win'),
                steal_ops.assign(Type='Steal Opportunity'),
                defensive.assign(Type='Defensive')
            ])
            csv = all_opportunities.to_csv(index=False)
            st.download_button("Download All Opportunities", csv, "opportunities.csv", "text/csv")
        
        with col2:
            json_data = json.dumps({
                'client_summary': summary['client'],
                'competitor_summary': summary['competitor'],
                'market_share': summary['market_share'],
                'quick_wins': quick_wins.to_dict('records'),
                'steal_opportunities': steal_ops.to_dict('records'),
                'defensive_keywords': defensive.to_dict('records'),
                'client_wins': client_wins.to_dict('records')
            }, indent=2, default=str)
            st.download_button("Download Full Analysis", json_data, "analysis.json", "application/json")
        
        with col3:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                quick_wins.to_excel(writer, sheet_name='Quick Wins', index=False)
                steal_ops.to_excel(writer, sheet_name='Steal Opportunities', index=False)
                defensive.to_excel(writer, sheet_name='Defensive Keywords', index=False)
                client_wins.to_excel(writer, sheet_name='Client Wins', index=False)
            output.seek(0)
            st.download_button("Download Excel Report", output.getvalue(), "keyword_gap_analysis.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.info("👋 Welcome to the Keyword Gap Analyzer!")
    st.markdown("""
    ### How to use this tool:
    
    1. **Upload CSV/Excel Files**: Upload your client and competitor organic performance reports
    2. **Configure AI**: Add your API keys to `config.toml` for AI-powered insights
    3. **Analyze**: Explore opportunities, wins, and strategic recommendations
    4. **Export**: Download your analysis in various formats
    
    ### Required Columns:
    - Keyword, Position, Previous position, Search Volume, Keyword Difficulty
    - CPC, URL, Traffic, Traffic (%), Traffic Cost, Competition
    - Number of Results, Trends, Timestamp, SERP Features by Keyword
    - Keyword Intents, Position Type
    
    ### Get Started:
    Upload your files using the sidebar to begin the analysis!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Keyword Gap Analyzer v1.0 | Built with Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)
