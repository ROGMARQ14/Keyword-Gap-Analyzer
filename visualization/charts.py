import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np


class ChartGenerator:
    """Generate interactive charts for keyword gap analysis."""
    
    @staticmethod
    def create_position_comparison_chart(client_df: pd.DataFrame, 
                                       competitor_df: pd.DataFrame) -> go.Figure:
        """Create scatter plot comparing positions between client and competitor."""
        
        # Merge dataframes on keyword
        merged_df = pd.merge(
            client_df[['Keyword', 'Position', 'Search Volume', 'Traffic Cost']],
            competitor_df[['Keyword', 'Position', 'Search Volume', 'Traffic Cost']],
            on='Keyword',
            suffixes=('_client', '_competitor')
        )
        
        fig = go.Figure()
        
        # Add scatter plot
        fig.add_trace(go.Scatter(
            x=merged_df['Position_client'],
            y=merged_df['Position_competitor'],
            mode='markers',
            marker=dict(
                size=np.log(merged_df['Search Volume_client'] + 1) * 3,
                color=merged_df['Traffic Cost_client'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Traffic Cost")
            ),
            text=merged_df['Keyword'],
            hovertemplate='<b>%{text}</b><br>' +
                          'Client Position: %{x}<br>' +
                          'Competitor Position: %{y}<br>' +
                          'Search Volume: %{marker.size}<br>' +
                          'Traffic Cost: %{marker.color}<extra></extra>'
        ))
        
        # Add diagonal line
        fig.add_trace(go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode='lines',
            line=dict(dash='dash', color='red'),
            name='Equal Position'
        ))
        
        fig.update_layout(
            title='Keyword Position Comparison: Client vs Competitor',
            xaxis_title='Client Position',
            yaxis_title='Competitor Position',
            height=600,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_opportunity_matrix(client_df: pd.DataFrame, 
                                competitor_df: pd.DataFrame) -> go.Figure:
        """Create opportunity matrix visualization."""
        
        # Calculate opportunity scores
        client_keywords = set(client_df['Keyword'])
        competitor_keywords = set(competitor_df['Keyword'])
        
        # Keywords where competitor ranks better
        opportunities = []
        for keyword in competitor_keywords:
            if keyword in client_keywords:
                client_pos = client_df[client_df['Keyword'] == keyword]['Position'].iloc[0]
                comp_pos = competitor_df[competitor_df['Keyword'] == keyword]['Position'].iloc[0]
                search_vol = competitor_df[competitor_df['Keyword'] == keyword]['Search Volume'].iloc[0]
                
                if comp_pos < client_pos:  # Competitor ranks better
                    opportunities.append({
                        'Keyword': keyword,
                        'Client Position': client_pos,
                        'Competitor Position': comp_pos,
                        'Search Volume': search_vol,
                        'Opportunity Score': search_vol / (client_pos - comp_pos + 1)
                    })
        
        if not opportunities:
            return go.Figure().add_annotation(
                text="No opportunities found",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        opp_df = pd.DataFrame(opportunities)
        
        fig = px.scatter(
            opp_df,
            x='Competitor Position',
            y='Client Position',
            size='Search Volume',
            color='Opportunity Score',
            hover_data=['Keyword'],
            title='Keyword Opportunity Matrix'
        )
        
        return fig
    
    @staticmethod
    def create_traffic_distribution_chart(client_df: pd.DataFrame, 
                                        competitor_df: pd.DataFrame) -> go.Figure:
        """Create traffic distribution comparison."""
        
        # Group by position ranges
        def categorize_position(pos):
            if pos <= 3:
                return 'Top 3'
            elif pos <= 10:
                return '4-10'
            elif pos <= 20:
                return '11-20'
            else:
                return '21+'
        
        client_df['Position Range'] = client_df['Position'].apply(categorize_position)
        competitor_df['Position Range'] = competitor_df['Position'].apply(categorize_position)
        
        client_traffic = client_df.groupby('Position Range')['Traffic'].sum()
        competitor_traffic = competitor_df.groupby('Position Range')['Traffic'].sum()
        
        fig = go.Figure(data=[
            go.Bar(name='Client', x=client_traffic.index, y=client_traffic.values),
            go.Bar(name='Competitor', x=competitor_traffic.index, y=competitor_traffic.values)
        ])
        
        fig.update_layout(
            title='Traffic Distribution by Position Range',
            xaxis_title='Position Range',
            yaxis_title='Total Traffic',
            barmode='group',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_keyword_intent_analysis(client_df: pd.DataFrame, 
                                     competitor_df: pd.DataFrame) -> go.Figure:
        """Create keyword intent analysis visualization."""
        
        # Count keywords by intent
        client_intents = client_df['Keyword Intents'].value_counts()
        competitor_intents = competitor_df['Keyword Intents'].value_counts()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Client',
            x=client_intents.index,
            y=client_intents.values,
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Competitor',
            x=competitor_intents.index,
            y=competitor_intents.values,
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title='Keyword Intent Distribution',
            xaxis_title='Intent Type',
            yaxis_title='Number of Keywords',
            barmode='group',
            height=400
        )
        
        return fig


def display_metrics_cards(summary):
    """Display key metrics in card format."""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Keywords",
            value=summary.get('total_keywords', 0),
            delta=summary.get('keyword_delta', 0)
        )
    
    with col2:
        st.metric(
            label="Total Traffic",
            value=f"{summary.get('total_traffic', 0):,.0f}",
            delta=summary.get('traffic_delta', 0)
        )
    
    with col3:
        st.metric(
            label="Avg Position",
            value=f"{summary.get('avg_position', 0):.1f}",
            delta=summary.get('position_delta', 0)
        )
    
    with col4:
        st.metric(
            label="Traffic Cost",
            value=f"${summary.get('traffic_cost', 0):,.0f}",
            delta=summary.get('cost_delta', 0)
        )


def create_competitive_analysis_table(client_df: pd.DataFrame, 
                                    competitor_df: pd.DataFrame) -> pd.DataFrame:
    """Create comprehensive competitive analysis table."""
    
    # Merge dataframes
    merged_df = pd.merge(
        client_df,
        competitor_df,
        on='Keyword',
        suffixes=('_client', '_competitor'),
        how='outer'
    )
    
    # Calculate metrics
    merged_df['Position_Diff'] = (
        merged_df['Position_client'] - merged_df['Position_competitor']
    )
    merged_df['Traffic_Diff'] = (
        merged_df['Traffic_client'] - merged_df['Traffic_competitor']
    )
    
    # Categorize opportunities
    def categorize_opportunity(row):
        if pd.isna(row['Position_client']):
            return 'New Opportunity'
        elif row['Position_competitor'] < row['Position_client']:
            if row['Position_client'] <= 10:
                return 'Quick Win'
            else:
                return 'Long-term Opportunity'
        else:
            return 'Defensive'
    
    merged_df['Opportunity_Type'] = merged_df.apply(categorize_opportunity, axis=1)
    
    # Select relevant columns
    result_df = merged_df[[
        'Keyword',
        'Position_client',
        'Position_competitor',
        'Search Volume_client',
        'Keyword Difficulty_client',
        'Traffic_client',
        'Traffic_competitor',
        'Position_Diff',
        'Traffic_Diff',
        'Opportunity_Type',
        'Keyword Intents_client',
        'SERP Features by Keyword_client'
    ]].copy()
    
    result_df.columns = [
        'Keyword',
        'Client Position',
        'Competitor Position',
        'Search Volume',
        'Keyword Difficulty',
        'Client Traffic',
        'Competitor Traffic',
        'Position Difference',
        'Traffic Difference',
        'Opportunity Type',
        'Intent',
        'SERP Features'
    ]
    
    return result_df
