import pandas as pd
from typing import Dict, Any
import streamlit as st

class KeywordGapAnalyzer:
    """Core analysis engine for keyword gap analysis."""
    
    def __init__(self):
        self.client_df = None
        self.competitor_df = None
        self.merged_df = None
    
    def load_data(self, client_df: pd.DataFrame, competitor_df: pd.DataFrame):
        """Load and prepare data for analysis."""
        # Remove duplicates by keeping the best position for each keyword
        self.client_df = self._deduplicate_keywords(client_df, 'client')
        self.competitor_df = self._deduplicate_keywords(competitor_df, 'competitor')
        self._merge_data()
    
    def _deduplicate_keywords(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        """Remove duplicate keywords by keeping the best position."""
        if df is None or df.empty:
            return df
        
        # Sort by position (ascending) and keep the first occurrence
        df_sorted = df.sort_values('Position')
        
        # Group by keyword and keep the first (best position)
        deduplicated = df_sorted.groupby('Keyword', as_index=False).first()
        
        # Add URL column to show multiple rankings
        if 'URL' in df.columns:
            # For keywords with multiple URLs, create a comma-separated list
            url_groups = df.groupby('Keyword')['URL'].apply(list).to_dict()
            deduplicated['All URLs'] = deduplicated['Keyword'].map(
                lambda x: ', '.join(url_groups.get(x, []))
            )
        
        return deduplicated
    
    def _merge_data(self):
        """Merge client and competitor data on keywords."""
        self.merged_df = pd.merge(
            self.client_df,
            self.competitor_df,
            on='Keyword',
            how='outer',
            suffixes=('_client', '_competitor')
        )
        
        # Fill missing values
        for col in ['Position_client', 'Position_competitor']:
            self.merged_df[col] = self.merged_df[col].fillna(999)
        
        # Ensure numeric types for key columns
        numeric_cols = ['Search Volume', 'Keyword Difficulty', 'CPC', 'Traffic', 
                       'Traffic Cost', 'Trends']
        for col in numeric_cols:
            for suffix in ['_client', '_competitor']:
                full_col = f"{col}{suffix}"
                if full_col in self.merged_df.columns:
                    self.merged_df[full_col] = pd.to_numeric(
                        self.merged_df[full_col], errors='coerce'
                    ).fillna(0)
    
    def get_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary metrics."""
        client_metrics = self._calculate_metrics(self.client_df)
        competitor_metrics = self._calculate_metrics(self.competitor_df)
        
        return {
            'client': client_metrics,
            'competitor': competitor_metrics,
            'market_share': self._calculate_market_share(),
            'opportunity_score': self._calculate_overall_opportunity()
        }
    
    def _calculate_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate key metrics for a dataset."""
        if df is None or df.empty:
            return {}
        
        return {
            'total_keywords': len(df),
            'avg_position': df['Position'].mean(),
            'total_traffic': df['Traffic'].sum(),
            'total_traffic_cost': df['Traffic Cost'].sum(),
            'top_3_keywords': len(df[df['Position'] <= 3]),
            'top_10_keywords': len(df[df['Position'] <= 10]),
            'keywords_11_plus': len(df[df['Position'] > 10])
        }
    
    def _calculate_market_share(self) -> Dict[str, float]:
        """Calculate market share between client and competitor."""
        client_traffic = self.client_df['Traffic'].sum() if not self.client_df.empty else 0
        competitor_traffic = self.competitor_df['Traffic'].sum() if not self.competitor_df.empty else 0
        
        total_traffic = client_traffic + competitor_traffic
        
        if total_traffic == 0:
            return {'client': 0, 'competitor': 0}
        
        return {
            'client': (client_traffic / total_traffic) * 100,
            'competitor': (competitor_traffic / total_traffic) * 100
        }
    
    def _calculate_overall_opportunity(self) -> float:
        """Calculate overall opportunity score."""
        if self.merged_df.empty:
            return 0
        
        # Sum of opportunity scores for keywords where competitor ranks better
        competitor_better = self.merged_df[
            self.merged_df['Position_competitor'] < self.merged_df['Position_client']
        ]
        
        if competitor_better.empty:
            return 0
        
        return competitor_better['Search Volume_competitor'].sum()
    
    def get_quick_wins(self) -> pd.DataFrame:
        """Identify quick win opportunities."""
        # Client ranks 6-10, competitor ranks 1-5
        quick_wins = self.merged_df[
            (self.merged_df['Position_client'].between(6, 10)) &
            (self.merged_df['Position_competitor'].between(1, 5)) &
            (self.merged_df['Search Volume_client'] > 100)
        ].copy()
        
        return self._format_opportunity_df(quick_wins, 'quick_win')
    
    def get_steal_opportunities(self) -> pd.DataFrame:
        """Identify keywords to steal from competitor."""
        # Client ranks 11+ or not ranking, competitor ranks 1-5
        steal_ops = self.merged_df[
            ((self.merged_df['Position_client'] > 10) | 
             (self.merged_df['Position_client'] == 999)) &
            (self.merged_df['Position_competitor'].between(1, 5)) &
            (self.merged_df['Search Volume_competitor'] > 100)
        ].copy()
        
        return self._format_opportunity_df(steal_ops, 'steal')
    
    def get_defensive_keywords(self) -> pd.DataFrame:
        """Identify keywords to defend."""
        # Client ranks 1-5, competitor is close behind
        defensive = self.merged_df[
            (self.merged_df['Position_client'].between(1, 5)) &
            (self.merged_df['Position_competitor'].between(1, 10)) &
            (self.merged_df['Position_competitor'] < self.merged_df['Position_client'] + 5)
        ].copy()
        
        return self._format_opportunity_df(defensive, 'defensive')
    
    def get_client_wins(self) -> pd.DataFrame:
        """Identify keywords where client outperforms competitor."""
        wins = self.merged_df[
            (self.merged_df['Position_client'] < self.merged_df['Position_competitor']) &
            (self.merged_df['Position_client'] <= 10)
        ].copy()
        
        return self._format_opportunity_df(wins, 'win')
    
    def get_content_gap_analysis(self) -> Dict[str, pd.DataFrame]:
        """Analyze content gaps by funnel stage."""
        content_gaps = {
            'tofu': self._get_funnel_keywords('Informational'),
            'mofu': self._get_funnel_keywords('Commercial'),
            'bofu': self._get_funnel_keywords('Transactional')
        }
        
        return content_gaps
    
    def _get_funnel_keywords(self, intent: str) -> pd.DataFrame:
        """Get keywords by funnel stage."""
        keywords = self.merged_df[
            self.merged_df['Keyword Intents_competitor'].str.contains(intent, na=False)
        ].copy()
        
        return self._format_opportunity_df(keywords, 'funnel')
    
    def _format_opportunity_df(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """Format opportunity data for display."""
        if df.empty:
            return pd.DataFrame()
        
        # Select and rename columns
        cols = {
            'Keyword': 'Keyword',
            'Search Volume_competitor': 'Search Volume',
            'Keyword Difficulty_competitor': 'Difficulty',
            'CPC_competitor': 'CPC',
            'Position_client': 'Client Position',
            'Position_competitor': 'Competitor Position',
            'Traffic_competitor': 'Competitor Traffic',
            'Traffic Cost_competitor': 'Traffic Cost',
            'Keyword Intents_competitor': 'Intent',
            'SERP Features by Keyword_competitor': 'SERP Features',
            'URL_client': 'Client URL',
            'URL_competitor': 'Competitor URL'
        }
        
        # Only include columns that exist
        available_cols = [col for col in cols.keys() if col in df.columns]
        result = df[available_cols].copy()
        result = result.rename(columns={k: v for k, v in cols.items() if k in available_cols})
        
        # Add priority score
        if 'Search Volume' in result.columns and 'Difficulty' in result.columns:
            result['Priority Score'] = (
                result['Search Volume'] * 0.4 +
                result.get('Traffic Cost', 0) * 0.3 +
                (100 - result['Difficulty']) * 0.3
            )
        
        # Sort by priority
        if 'Priority Score' in result.columns:
            result = result.sort_values('Priority Score', ascending=False)
        
        return result
    
    def get_trending_keywords(self) -> pd.DataFrame:
        """Identify trending keywords."""
        # Ensure Trends_competitor is numeric
        self.merged_df['Trends_competitor'] = pd.to_numeric(
            self.merged_df['Trends_competitor'], errors='coerce'
        ).fillna(0)
        
        trending = self.merged_df[
            (self.merged_df['Trends_competitor'] > 0) &
            (self.merged_df['Search Volume_competitor'] > 100)
        ].copy()
        
        return self._format_opportunity_df(trending, 'trending')
