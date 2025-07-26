import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Keyword Gap Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🔍 Keyword Gap Analyzer")
st.markdown("**Enterprise SEO Competitive Analysis Tool**")
st.markdown("Upload your client and competitor keyword data to generate comprehensive gap analysis.")

# Sidebar for file uploads
with st.sidebar:
    st.header("📁 Data Upload")
    
    client_file = st.file_uploader(
        "Upload Client CSV File",
        type=['csv'],
        key="client_file"
    )
    
    competitor_file = st.file_uploader(
        "Upload Competitor CSV File", 
        type=['csv'],
        key="competitor_file"
    )
    
    st.divider()
    
    st.header("⚙️ Analysis Settings")
    
    min_search_volume = st.slider(
        "Minimum Search Volume",
        min_value=0,
        max_value=10000,
        value=100,
        step=50
    )
    
    max_keyword_difficulty = st.slider(
        "Maximum Keyword Difficulty",
        min_value=0,
        max_value=100,
        value=70,
        step=5
    )

def load_and_validate_csv(file):
    """Load and validate CSV file with robust error handling."""
    if file is None:
        return None
    
    try:
        # Try different CSV parsing approaches
        df = None
        
        # Method 1: Try semicolon delimiter (common in European CSVs)
        try:
            file.seek(0)
            df = pd.read_csv(file, sep=';', on_bad_lines='skip', engine='python')
        except Exception:
            # Method 2: Try comma delimiter
            file.seek(0)
            df = pd.read_csv(file, sep=',', on_bad_lines='skip', engine='python')
        
        if df is None or df.empty:
            st.error("Could not load the CSV file. Please check the file format.")
            return None
        
        # Display actual columns for debugging
        st.info(f"Loaded file with columns: {', '.join(df.columns.tolist())}")
        
        # Map common column variations - handle exact matches first
        column_mapping = {
            'Keyword': ['Keyword', 'keyword', 'Keywords', 'keywords', 'Search Term', 'search term'],
            'Position': ['Position', 'position', 'Rank', 'rank', 'Current Position'],
            'Previous position': ['Previous position', 'Previous Position', 'Previous Rank', 'Last Position'],
            'Search Volume': ['Search Volume', 'search volume', 'Volume', 'volume', 'Monthly Searches'],
            'Keyword Difficulty': ['Keyword Difficulty', 'Difficulty', 'KD', 'Competition Score'],
            'CPC': ['CPC', 'Cost Per Click', 'cost per click', 'Avg CPC'],
            'URL': ['URL', 'url', 'Landing Page', 'landing page'],
            'Traffic': ['Traffic', 'traffic', 'Est Traffic', 'Estimated Traffic'],
            'Traffic (%)': ['Traffic (%)', 'Traffic %', 'traffic %', 'Traffic Percentage'],
            'Traffic Cost': ['Traffic Cost', 'traffic cost', 'Value', 'Cost'],
            'Competition': ['Competition', 'competition', 'Competitive Density'],
            'Number of Results': ['Number of Results', 'Results', 'SERP Results'],
            'Trends': ['Trends', 'trends', 'Search Trend'],
            'Timestamp': ['Timestamp', 'Date', 'date'],
            'SERP Features by Keyword': ['SERP Features', 'SERP Features by Keyword', 'Features'],
            'Keyword Intents': ['Keyword Intents', 'Intent', 'Search Intent'],
            'Position Type': ['Position Type', 'Type', 'Ranking Type']
        }
        
        # Create new dataframe with standardized columns
        standardized_df = pd.DataFrame()
        
        # Handle exact column matches first
        for standard_col, possible_cols in column_mapping.items():
            for col in possible_cols:
                if col in df.columns:
                    standardized_df[standard_col] = df[col]
                    break
        
        # Check if we have the essential columns
        essential_cols = ['Keyword', 'Position', 'Search Volume', 'Keyword Difficulty']
        missing_essential = set(essential_cols) - set(standardized_df.columns)
        
        if missing_essential:
            st.error(f"Missing essential columns: {missing_essential}")
            st.info("Please ensure your CSV has at least: Keyword, Position, Search Volume, Keyword Difficulty")
            return None
        
        # Clean data
        numeric_cols = ['Position', 'Previous position', 'Search Volume',
                       'Keyword Difficulty', 'CPC', 'Traffic', 'Traffic (%)',
                       'Traffic Cost', 'Competition', 'Number of Results']
        
        for col in numeric_cols:
            if col in standardized_df.columns:
                standardized_df[col] = pd.to_numeric(standardized_df[col], errors='coerce')
        
        # Fill missing values
        if 'Previous position' in standardized_df.columns:
            standardized_df['Previous position'] = standardized_df['Previous position'].fillna(standardized_df['Position'])
        else:
            standardized_df['Previous position'] = standardized_df['Position']
        
        if 'Keyword Difficulty' in standardized_df.columns:
            standardized_df['Keyword Difficulty'] = standardized_df['Keyword Difficulty'].fillna(50)
        
        if 'CPC' in standardized_df.columns:
            standardized_df['CPC'] = standardized_df['CPC'].fillna(0)
        
        # Create calculated fields
        standardized_df['Position Change'] = standardized_df['Previous position'] - standardized_df['Position']
        standardized_df['Opportunity Score'] = (standardized_df['Search Volume'] * 0.1) / (standardized_df['Keyword Difficulty'] + 1)
        
        return standardized_df
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        st.info("Please ensure your CSV file is properly formatted with the required columns.")
        return None

def analyze_keyword_gaps(client_df, competitor_df, min_volume, max_difficulty):
    """Perform comprehensive keyword gap analysis."""
    
    # Filter by settings
    client_filtered = client_df[
        (client_df['Search Volume'] >= min_volume) & 
        (client_df['Keyword Difficulty'] <= max_difficulty)
    ].copy()
    
    competitor_filtered = competitor_df[
        (competitor_df['Search Volume'] >= min_volume) & 
        (competitor_df['Keyword Difficulty'] <= max_difficulty)
    ].copy()
    
    # Merge dataframes on keyword
    merged_df = pd.merge(
        client_filtered[['Keyword', 'Position', 'Search Volume', 'Keyword Difficulty', 'CPC']],
        competitor_filtered[['Keyword', 'Position', 'Search Volume', 'Keyword Difficulty', 'CPC']],
        on='Keyword',
        suffixes=('_client', '_competitor'),
        how='outer'
    )
    
    # Analysis categories
    analysis = {
        'quick_wins': [],
        'steal_opportunities': [],
        'client_wins': [],
        'content_gaps': []
    }
    
    for _, row in merged_df.iterrows():
        client_pos = row['Position_client'] if pd.notna(row['Position_client']) else 999
        competitor_pos = row['Position_competitor'] if pd.notna(row['Position_competitor']) else 999
        
        # Quick wins: client ranks 6-10, competitor ranks 1-5
        if 6 <= client_pos <= 10 and 1 <= competitor_pos <= 5:
            analysis['quick_wins'].append({
                'Keyword': row['Keyword'],
                'Client Position': int(client_pos),
                'Competitor Position': int(competitor_pos),
                'Search Volume': int(row['Search Volume_client']),
                'Difficulty': int(row['Keyword Difficulty_client']),
                'Opportunity Score': round(row['Search Volume_client'] / (row['Keyword Difficulty_client'] + 1), 2)
            })
        
        # Steal opportunities: competitor ranks 1-3, client ranks 11+ or missing
        elif 1 <= competitor_pos <= 3 and (client_pos > 11 or client_pos == 999):
            analysis['steal_opportunities'].append({
                'Keyword': row['Keyword'],
                'Client Position': 'Not ranking' if client_pos == 999 else int(client_pos),
                'Competitor Position': int(competitor_pos),
                'Search Volume': int(row['Search Volume_competitor']),
                'Difficulty': int(row['Keyword Difficulty_competitor']),
                'CPC': round(row['CPC_competitor'], 2)
            })
        
        # Client wins: client ranks better than competitor
        elif client_pos < competitor_pos and client_pos <= 10:
            analysis['client_wins'].append({
                'Keyword': row['Keyword'],
                'Client Position': int(client_pos),
                'Competitor Position': int(competitor_pos),
                'Search Volume': int(row['Search Volume_client']),
                'Advantage': int(competitor_pos - client_pos)
            })
    
    return analysis

# Main application
if client_file and competitor_file:
    client_df = load_and_validate_csv(client_file)
    competitor_df = load_and_validate_csv(competitor_file)
    
    if client_df is not None and competitor_df is not None:
        st.success("✅ Files loaded successfully!")
        
        # Display data summary
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Client Keywords", len(client_df))
        with col2:
            st.metric("Competitor Keywords", len(competitor_df))
        
        # Analysis
        analysis = analyze_keyword_gaps(client_df, competitor_df, min_search_volume, max_keyword_difficulty)
        
        # Executive Summary
        st.header("📊 Executive Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Quick Wins", len(analysis['quick_wins']))
        with col2:
            st.metric("Steal Opportunities", len(analysis['steal_opportunities']))
        with col3:
            st.metric("Client Wins", len(analysis['client_wins']))
        with col4:
            total_opportunities = len(analysis['quick_wins']) + len(analysis['steal_opportunities'])
            st.metric("Total Opportunities", total_opportunities)
        
        # Detailed Analysis
        st.header("🔍 Detailed Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Quick Wins", "Steal Opportunities", "Client Wins"])
        
        with tab1:
            if analysis['quick_wins']:
                quick_wins_df = pd.DataFrame(analysis['quick_wins'])
                quick_wins_df = quick_wins_df.sort_values('Opportunity Score', ascending=False)
                st.dataframe(quick_wins_df, use_container_width=True)
                
                # Download button
                csv = quick_wins_df.to_csv(index=False)
                st.download_button(
                    label="Download Quick Wins CSV",
                    data=csv,
                    file_name="quick_wins.csv",
                    mime="text/csv"
                )
            else:
                st.info("No quick wins identified.")
        
        with tab2:
            if analysis['steal_opportunities']:
                steal_df = pd.DataFrame(analysis['steal_opportunities'])
                steal_df = steal_df.sort_values('Search Volume', ascending=False)
                st.dataframe(steal_df, use_container_width=True)
                
                # Download button
                csv = steal_df.to_csv(index=False)
                st.download_button(
                    label="Download Steal Opportunities CSV",
                    data=csv,
                    file_name="steal_opportunities.csv",
                    mime="text/csv"
                )
            else:
                st.info("No steal opportunities identified.")
        
        with tab3:
            if analysis['client_wins']:
                wins_df = pd.DataFrame(analysis['client_wins'])
                wins_df = wins_df.sort_values('Advantage', ascending=False)
                st.dataframe(wins_df, use_container_width=True)
                
                # Download button
                csv = wins_df.to_csv(index=False)
                st.download_button(
                    label="Download Client Wins CSV",
                    data=csv,
                    file_name="client_wins.csv",
                    mime="text/csv"
                )
            else:
                st.info("No client wins identified.")

else:
    st.info("👆 Please upload both client and competitor CSV files to begin analysis.")

# Footer
st.divider()
st.markdown("""
**📋 Instructions:**
1. Upload your client keyword performance CSV
2. Upload your competitor keyword performance CSV  
3. Configure analysis parameters in the sidebar
4. Review the generated insights and recommendations
5. Export results for your SEO strategy
""")
