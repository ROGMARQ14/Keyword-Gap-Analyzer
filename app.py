import streamlit as st
import pandas as pd
from utils.data_loader import DataLoader
from core.analyzer import KeywordGapAnalyzer
from utils.ai_analyzer import AIAnalyzer
from visualization.charts import ChartGenerator
import io

# Page configuration
st.set_page_config(
    page_title="Keyword Gap Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .opportunity-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_analyzer():
    return KeywordGapAnalyzer()

@st.cache_resource
def init_ai_analyzer():
    return AIAnalyzer()

analyzer = init_analyzer()
ai_analyzer = init_ai_analyzer()

# Header
st.markdown('<div class="main-header">🔍 Keyword Gap Analyzer</div>', 
            unsafe_allow_html=True)
st.markdown("Enterprise-ready competitive intelligence for SEO strategy")

# Sidebar
with st.sidebar:
    st.header("📁 Data Upload")
    
    # File uploaders
    client_file = st.file_uploader(
        "Upload Client CSV", 
        type=['csv'], 
        key="client_file"
    )
    
    competitor_file = st.file_uploader(
        "Upload Competitor CSV", 
        type=['csv'], 
        key="competitor_file"
    )
    
    st.divider()
    
    # Configuration
    st.header("⚙️ Configuration")
    
    min_volume = st.slider(
        "Minimum Search Volume",
        min_value=0,
        max_value=10000,
        value=100,
        step=50
    )
    
    max_difficulty = st.slider(
        "Maximum Keyword Difficulty",
        min_value=0,
        max_value=100,
        value=70,
        step=5
    )
    
    st.divider()
    
    # AI Model Selection
    st.header("🤖 AI Analysis")
    
    available_models = []
    for model in ["openai", "anthropic", "gemini"]:
        if ai_analyzer.is_configured(model):
            available_models.append(model)
    
    if available_models:
        selected_model = st.selectbox(
            "Select AI Model",
            available_models,
            format_func=lambda x: x.title()
        )
        
        generate_ai_insights = st.button(
            "Generate AI Insights",
            type="primary",
            use_container_width=True
        )
    else:
        st.warning("No AI models configured. Add API keys to config.toml")
        selected_model = None
        generate_ai_insights = False

# Main content
if client_file and competitor_file:
    # Load data
    with st.spinner("Loading and analyzing data..."):
        client_df = DataLoader.load_csv(client_file)
        competitor_df = DataLoader.load_csv(competitor_file)
        
        if client_df is not None and competitor_df is not None:
            # Filter data based on configuration
            client_df = client_df[client_df['Search Volume'] >= min_volume]
            client_df = client_df[client_df['Keyword Difficulty'] <= max_difficulty]
            
            competitor_df = competitor_df[competitor_df['Search Volume'] >= min_volume]
            competitor_df = competitor_df[competitor_df['Keyword Difficulty'] <= max_difficulty]
            
            # Load data into analyzer
            analyzer.load_data(client_df, competitor_df)
            
            # Get analysis results
            summary = analyzer.get_executive_summary()
            quick_wins = analyzer.get_quick_wins()
            steal_ops = analyzer.get_steal_opportunities()
            defensive = analyzer.get_defensive_keywords()
            client_wins = analyzer.get_client_wins()
            content_gaps = analyzer.get_content_gap_analysis()
            priority_matrix = analyzer.get_priority_matrix()
            
            # Executive Summary
            st.header("📊 Executive Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Client Keywords",
                    f"{summary['client']['total_keywords']:,}",
                    delta=f"{summary['client']['total_keywords'] - summary['competitor']['total_keywords']:,} vs competitor"
                )
            
            with col2:
                st.metric(
                    "Client Avg Position",
                    f"{summary['client']['avg_position']:.1f}",
                    delta=f"{summary['client']['avg_position'] - summary['competitor']['avg_position']:.1f}"
                )
            
            with col3:
                st.metric(
                    "Client Traffic",
                    f"{summary['client']['total_traffic']:,}",
                    delta=f"{((summary['client']['total_traffic'] / (summary['client']['total_traffic'] + summary['competitor']['total_traffic'])) * 100):.1f}% share"
                )
            
            with col4:
                st.metric(
                    "Traffic Value",
                    f"${summary['client']['total_traffic_cost']:,}",
                    delta=f"${summary['client']['total_traffic_cost'] - summary['competitor']['total_traffic_cost']:,}"
                )
            
            # Visualizations
            st.header("📈 Visual Analysis")
            
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Opportunities", "Content Gaps", "AI Insights"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1 = ChartGenerator.create_position_comparison_chart(
                        client_df, competitor_df
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    fig2 = ChartGenerator.create_market_share_chart(summary)
                    st.plotly_chart(fig2, use_container_width=True)
            
            with tab2:
                if not priority_matrix.empty:
                    fig3 = ChartGenerator.create_opportunity_matrix(priority_matrix)
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("No opportunities found with current filters")
            
            with tab3:
                fig4 = ChartGenerator.create_funnel_gap_chart(content_gaps)
                st.plotly_chart(fig4, use_container_width=True)
                
                trending = analyzer.get_trending_keywords()
                if not trending.empty:
                    fig5 = ChartGenerator.create_trend_analysis_chart(trending)
                    st.plotly_chart(fig5, use_container_width=True)
            
            with tab4:
                if generate_ai_insights and selected_model:
                    with st.spinner("Generating AI insights..."):
                        analysis_data = {
                            'client_total_keywords': summary['client']['total_keywords'],
                            'client_avg_position': summary['client']['avg_position'],
                            'client_total_traffic': summary['client']['total_traffic'],
                            'client_traffic_cost': summary['client']['total_traffic_cost'],
                            'competitor_total_keywords': summary['competitor']['total_keywords'],
                            'competitor_avg_position': summary['competitor']['avg_position'],
                            'competitor_total_traffic': summary['competitor']['total_traffic'],
                            'competitor_traffic_cost': summary['competitor']['total_traffic_cost'],
                            'quick_wins': quick_wins,
                            'steal_opportunities': steal_ops,
                            'defensive_keywords': defensive
                        }
                        
                        insights = ai_analyzer.generate_insights(
                            analysis_data, selected_model
                        )
                        
                        st.markdown("### 🤖 AI Strategic Analysis")
                        st.markdown(insights)
                else:
                    st.info("Click 'Generate AI Insights' to get strategic recommendations")
            
            # Detailed Tables
            st.header("📋 Detailed Analysis")
            
            # Quick Wins
            if not quick_wins.empty:
                with st.expander(f"🚀 Quick Wins ({len(quick_wins)} opportunities)"):
                    display_cols = ['Keyword', 'Position_client', 'Position_competitor', 
                                  'Search Volume_client', 'Keyword Difficulty_client', 
                                  'Traffic Cost_client', 'Opportunity Score']
                    st.dataframe(
                        quick_wins[display_cols].head(20),
                        use_container_width=True
                    )
                    
                    csv = quick_wins[display_cols].to_csv(index=False)
                    st.download_button(
                        label="Download Quick Wins CSV",
                        data=csv,
                        file_name="quick_wins.csv",
                        mime="text/csv"
                    )
            
            # Steal Opportunities
            if not steal_ops.empty:
                with st.expander(f"💰 Steal Opportunities ({len(steal_ops)} opportunities)"):
                    display_cols = ['Keyword', 'Position_competitor', 'Search Volume_competitor', 
                                  'Keyword Difficulty_competitor', 'Traffic Cost_competitor', 
                                  'Potential Traffic', 'Potential Value']
                    st.dataframe(
                        steal_ops[display_cols].head(20),
                        use_container_width=True
                    )
                    
                    csv = steal_ops[display_cols].to_csv(index=False)
                    st.download_button(
                        label="Download Steal Opportunities CSV",
                        data=csv,
                        file_name="steal_opportunities.csv",
                        mime="text/csv"
                    )
            
            # Client Wins
            if not client_wins.empty:
                with st.expander(f"🏆 Client Wins ({len(client_wins)} keywords)"):
                    display_cols = ['Keyword', 'Position_client', 'Position_competitor', 
                                  'Search Volume_client', 'Traffic Cost_client', 'Win Margin']
                    st.dataframe(
                        client_wins[display_cols].head(20),
                        use_container_width=True
                    )
            
            # Defensive Keywords
            if not defensive.empty:
                with st.expander(f"🛡️ Defensive Keywords ({len(defensive)} keywords)"):
                    display_cols = ['Keyword', 'Position_client', 'Position_competitor', 
                                  'Search Volume_client', 'Traffic Cost_client', 'Threat Level']
                    st.dataframe(
                        defensive[display_cols].head(20),
                        use_container_width=True
                    )
            
            # Content Gaps
            for stage, gaps in content_gaps.items():
                if not gaps.empty:
                    with st.expander(f"📄 {stage.upper()} Content Gaps ({len(gaps)} keywords)"):
                        display_cols = ['Keyword', 'Position_competitor', 
                                      'Search Volume_competitor', 'Keyword Difficulty_competitor']
                        st.dataframe(
                            gaps[display_cols].head(10),
                            use_container_width=True
                        )
            
            # Full Export
            st.divider()
            st.header("📤 Export All Data")
            
            if not priority_matrix.empty:
                csv_all = priority_matrix.to_csv(index=False)
                st.download_button(
                    label="Download Complete Analysis (CSV)",
                    data=csv_all,
                    file_name="keyword_gap_analysis.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Excel export
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    priority_matrix.to_excel(writer, sheet_name='Priority Matrix', index=False)
                    if not quick_wins.empty:
                        quick_wins.to_excel(writer, sheet_name='Quick Wins', index=False)
                    if not steal_ops.empty:
                        steal_ops.to_excel(writer, sheet_name='Steal Opportunities', index=False)
                    if not client_wins.empty:
                        client_wins.to_excel(writer, sheet_name='Client Wins', index=False)
                    if not defensive.empty:
                        defensive.to_excel(writer, sheet_name='Defensive Keywords', index=False)
                
                output.seek(0)
                st.download_button(
                    label="Download Excel Report",
                    data=output.getvalue(),
                    file_name="keyword_gap_analysis.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
        else:
            st.error("Failed to load data. Please check file formats.")
    
else:
    st.info("👆 Please upload both client and competitor CSV files to begin analysis")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Built with ❤️ for SEO professionals | 
    <a href="https://github.com/your-repo">View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
