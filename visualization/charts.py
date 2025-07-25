import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict


class ChartGenerator:
    """Generate interactive visualizations for keyword analysis."""
    
    @staticmethod
    def create_position_comparison_chart(client_df: pd.DataFrame, 
                                       competitor_df: pd.DataFrame) -> go.Figure:
        """Create position distribution comparison."""
        
        client_positions = client_df['Position'].value_counts().sort_index()
        competitor_positions = competitor_df['Position'].value_counts().sort_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=client_positions.index,
            y=client_positions.values,
            mode='lines+markers',
            name='Client',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=competitor_positions.index,
            y=competitor_positions.values,
            mode='lines+markers',
            name='Competitor',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Position Distribution Comparison',
            xaxis_title='Position',
            yaxis_title='Number of Keywords',
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_opportunity_matrix(opportunities_df: pd.DataFrame) -> go.Figure:
        """Create opportunity matrix visualization."""
        if opportunities_df.empty:
            return go.Figure()
        
        fig = px.scatter(
            opportunities_df,
            x='Keyword Difficulty_client',
            y='Search Volume_client',
            color='Type',
            size='Traffic Cost_client',
            hover_data=['Keyword', 'Position_client', 'Position_competitor'],
            title='Opportunity Matrix: Difficulty vs Volume'
        )
        
        fig.update_layout(
            height=500,
            template='plotly_white',
            xaxis_title='Keyword Difficulty',
            yaxis_title='Search Volume'
        )
        
        return fig
    
    @staticmethod
    def create_market_share_chart(summary: Dict) -> go.Figure:
        """Create market share visualization."""
        
        labels = ['Client', 'Competitor']
        values = [summary['market_share']['client'], 
                 summary['market_share']['competitor']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=['#1f77b4', '#ff7f0e'])
        )])
        
        fig.update_layout(
            title='Traffic Market Share',
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_funnel_gap_chart(content_gaps: Dict[str, pd.DataFrame]) -> go.Figure:
        """Create content funnel gap visualization."""
        
        stages = ['TOFU', 'MOFU', 'BOFU']
        client_counts = []
        competitor_counts = []
        
        for stage in stages:
            stage_lower = stage.lower()
            if stage_lower in content_gaps:
                client_count = len(content_gaps[stage_lower])
                competitor_count = len(content_gaps[stage_lower])
                client_counts.append(client_count)
                competitor_counts.append(competitor_count)
            else:
                client_counts.append(0)
                competitor_counts.append(0)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Client',
            x=stages,
            y=client_counts,
            marker_color='#1f77b4'
        ))
        
        fig.add_trace(go.Bar(
            name='Competitor',
            x=stages,
            y=competitor_counts,
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            title='Content Gap Analysis by Funnel Stage',
            xaxis_title='Funnel Stage',
            yaxis_title='Number of Keywords',
            height=400,
            template='plotly_white',
            barmode='group'
        )
        
        return fig
    
    @staticmethod
    def create_trend_analysis_chart(trending_df: pd.DataFrame) -> go.Figure:
        """Create trending keywords visualization."""
        if trending_df.empty:
            return go.Figure()
        
        top_trending = trending_df.nlargest(10, 'Trend Score')
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=top_trending['Keyword'],
            y=top_trending['Trend Score'],
            marker_color='#2ca02c',
            text=top_trending['Position Change'].astype(str) + ' positions',
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Top 10 Trending Keywords',
            xaxis_title='Keyword',
            yaxis_title='Trend Score',
            height=400,
            template='plotly_white',
            xaxis_tickangle=-45
        )
        
        return fig
    
    @staticmethod
    def create_priority_heatmap(priority_df: pd.DataFrame) -> go.Figure:
        """Create priority heatmap for opportunities."""
        if priority_df.empty:
            return go.Figure()
        
        # Create pivot table
        pivot_data = priority_df.pivot_table(
            values='Priority Score',
            index='Type',
            columns='Priority',
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlGn',
            text=pivot_data.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 12}
        ))
        
        fig.update_layout(
            title='Opportunity Priority Heatmap',
            height=400,
            template='plotly_white'
        )
        
        return fig
