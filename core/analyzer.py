import pandas as pd
import numpy as np
from typing import Dict, List, Any
import streamlit as st


class KeywordGapAnalyzer:
    """Core analysis engine for keyword gap analysis."""
    
    def __init__(self):
        self.client_df = None
        self.competitor_df = None
        self.merged_df = None
    
    def load_data(self, client_df: pd.DataFrame, competitor_df: pd.DataFrame):
        """Load and merge client and competitor data."""
        self.client_df = client_df
        self.competitor_df = competitor_df
        
        # Merge data on keyword
        self.merged_df = pd.merge(
            client_df[['Keyword', 'Position', 'Search Volume', 'Keyword Difficulty', 
                      'CPC', 'Traffic', 'Traffic Cost', 'Keyword Intents', 'URL']],
            competitor_df[['Keyword', 'Position', 'Search Volume', 'Keyword Difficulty', 
                          'CPC', 'Traffic', 'Traffic Cost', 'URL']],
            on='Keyword',
            suffixes=('_client', '_competitor'),
            how='outer'
        )
        
        # Fill NaN values
        self.merged_df['Position_client'] = self.merged_df['Position_client'].fillna(100)
        self.merged_df['Position_competitor'] = self.merged_df['Position_competitor'].fillna(100)
    
    def get_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary metrics."""
        
        client_metrics = {
            'total_keywords': len(self.client_df),
            'avg_position': self.client_df['Position'].mean(),
            'total_traffic': self.client_df['Traffic'].sum(),
            'total_traffic_cost': self.client_df['Traffic Cost'].sum()
        }
        
        competitor_metrics = {
            'total_keywords': len(self.competitor_df),
            'avg_position': self.competitor_df['Position'].mean(),
            'total_traffic': self.competitor_df['Traffic'].sum(),
            'total_traffic_cost': self.competitor_df['Traffic Cost'].sum()
        }
        
        total_traffic = client_metrics['total_traffic'] + competitor_metrics['total_traffic']
        market_share = {
            'client': (client_metrics['total_traffic'] / total_traffic * 100) if total_traffic > 0 else 0,
            'competitor': (competitor_metrics['total_traffic'] / total_traffic * 100) if total_traffic > 0 else 0
        }
        
        # Calculate opportunity score
        quick_wins = self.get_quick_wins()
        steal_ops = self.get_steal_opportunities()
        opportunity_score = len(quick_wins) + len(steal_ops)
        
        return {
            'client': client_metrics,
            'competitor': competitor_metrics,
            'market_share': market_share,
            'opportunity_score': opportunity_score
        }
    
    def get_quick_wins(self) -> pd.DataFrame:
        """Identify quick win opportunities."""
        if self.merged_df is None:
            return pd.DataFrame()
        
        # Client ranks 6-10, competitor ranks 1-5
        quick_wins = self.merged_df[
            (self.merged_df['Position_client'] >= 6) & 
            (self.merged_df['Position_client'] <= 10) &
            (self.merged_df['Position_competitor'] >= 1) & 
            (self.merged_df['Position_competitor'] <= 5) &
            (self.merged_df['Search Volume_client'] >= 100) &
            (self.merged_df['Keyword Difficulty_client'] <= 70)
        ].copy()
        
        # Sort by opportunity score
        quick_wins['Opportunity Score'] = (
            quick_wins['Search Volume_client'] * 
            (1 - quick_wins['Keyword Difficulty_client'] / 100)
        )
        
        return quick_wins.sort_values('Opportunity Score', ascending=False)
    
    def get_steal_opportunities(self) -> pd.DataFrame:
        """Identify high-value keywords to steal from competitor."""
        if self.merged_df is None:
            return pd.DataFrame()
        
        # Client not ranking or ranks poorly, competitor ranks 1-5
        steal_ops = self.merged_df[
            ((self.merged_df['Position_client'] > 10) | 
             (self.merged_df['Position_client'] == 100)) &
            (self.merged_df['Position_competitor'] >= 1) & 
            (self.merged_df['Position_competitor'] <= 5) &
            (self.merged_df['Search Volume_competitor'] >= 100)
        ].copy()
        
        # Calculate potential value
        steal_ops['Potential Traffic'] = steal_ops['Traffic_competitor'] * 0.3
        steal_ops['Potential Value'] = steal_ops['Traffic Cost_competitor'] * 0.3
        
        return steal_ops.sort_values('Traffic_competitor', ascending=False)
    
    def get_defensive_keywords(self) -> pd.DataFrame:
        """Identify keywords to defend against competitor gains."""
        if self.merged_df is None:
            return pd.DataFrame()
        
        # Client ranks 1-5, competitor close behind
        defensive = self.merged_df[
            (self.merged_df['Position_client'] >= 1) & 
            (self.merged_df['Position_client'] <= 5) &
            (self.merged_df['Position_competitor'] >= 2) & 
            (self.merged_df['Position_competitor'] <= 10) &
            (self.merged_df['Search Volume_client'] >= 100)
        ].copy()
        
        # Calculate threat level
        defensive['Threat Level'] = (
            defensive['Search Volume_client'] * 
            (1 / defensive['Position_competitor'])
        )
        
        return defensive.sort_values('Threat Level', ascending=False)
    
    def get_client_wins(self) -> pd.DataFrame:
        """Identify keywords where client outperforms competitor."""
        if self.merged_df is None:
            return pd.DataFrame()
        
        # Client ranks better than competitor
        client_wins = self.merged_df[
            (self.merged_df['Position_client'] < self.merged_df['Position_competitor']) &
            (self.merged_df['Position_client'] <= 10)
        ].copy()
        
        # Calculate win margin
        client_wins['Win Margin'] = (
            client_wins['Position_competitor'] - client_wins['Position_client']
        )
        
        return client_wins.sort_values('Win Margin', ascending=False)
    
    def get_trending_keywords(self) -> pd.DataFrame:
        """Identify trending keywords with growth potential."""
        if self.client_df is None:
            return pd.DataFrame()
        
        # Simple trending based on position improvement
        trending = self.client_df[
            (self.client_df['Position Change'] > 0) &
            (self.client_df['Search Volume'] >= 100)
        ].copy()
        
        trending['Trend Score'] = (
            trending['Position Change'] * 
            trending['Search Volume'] / 
            (trending['Keyword Difficulty'] + 1)
        )
        
        return trending.sort_values('Trend Score', ascending=False)
    
    def get_content_gap_analysis(self) -> Dict[str, pd.DataFrame]:
        """Analyze content gaps by funnel stage."""
        if self.merged_df is None:
            return {'tofu': pd.DataFrame(), 'mofu': pd.DataFrame(), 'bofu': pd.DataFrame()}
        
        # Map intents to funnel stages
        def map_intent_to_funnel(intent):
            if pd.isna(intent):
                return 'tofu'
            
            intent_str = str(intent).lower()
            if any(word in intent_str for word in ['informational', 'how', 'what', 'guide']):
                return 'tofu'
            elif any(word in intent_str for word in ['commercial', 'best', 'review', 'vs']):
                return 'mofu'
            elif any(word in intent_str for word in ['transactional', 'buy', 'price', 'deal']):
                return 'bofu'
            else:
                return 'tofu'
        
        # Apply mapping
        self.merged_df['Funnel Stage'] = self.merged_df['Keyword Intents_client'].apply(
            map_intent_to_funnel
        )
        
        # Get gaps for each stage
        gaps = {}
        for stage in ['tofu', 'mofu', 'bofu']:
            stage_gaps = self.merged_df[
                (self.merged_df['Funnel Stage'] == stage) &
                ((self.merged_df['Position_client'] > 10) | 
                 (self.merged_df['Position_client'] == 100)) &
                (self.merged_df['Position_competitor'] <= 5)
            ]
            gaps[stage] = stage_gaps.sort_values('Search Volume_competitor', ascending=False)
        
        return gaps
    
    def get_priority_matrix(self) -> pd.DataFrame:
        """Create priority matrix for all opportunities."""
        quick_wins = self.get_quick_wins()
        steal_ops = self.get_steal_opportunities()
        defensive = self.get_defensive_keywords()
        
        # Combine all opportunities
        all_opps = []
        
        if not quick_wins.empty:
            quick_wins['Type'] = 'Quick Win'
            quick_wins['Priority'] = 'High'
            all_opps.append(quick_wins)
        
        if not steal_ops.empty:
            steal_ops['Type'] = 'Steal Opportunity'
            steal_ops['Priority'] = 'Medium'
            all_opps.append(steal_ops)
        
        if not defensive.empty:
            defensive['Type'] = 'Defensive'
            defensive['Priority'] = 'High'
            all_opps.append(defensive)
        
        if all_opps:
            combined = pd.concat(all_opps, ignore_index=True)
            combined['Priority Score'] = (
                combined['Search Volume_client'].fillna(combined['Search Volume_competitor']) * 0.4 +
                combined['Traffic Cost_client'].fillna(combined['Traffic Cost_competitor']) * 0.3 +
                (100 - combined['Keyword Difficulty_client'].fillna(
                    combined['Keyword Difficulty_competitor'])) * 0.3
            )
            return combined.sort_values('Priority Score', ascending=False)
        
        return pd.DataFrame()
