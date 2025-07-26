import pandas as pd
import streamlit as st
from typing import Optional


class DataLoader:
    """Handles loading and validation of CSV files for keyword analysis."""
    
    # Flexible column mapping for real-world CSV files
    COLUMN_MAPPING = {
        'Keyword': ['Keyword', 'keyword', 'Keywords', 'keywords', 'Search Term', 'search term'],
        'Position': ['Position', 'position', 'Rank', 'rank', 'Current Position'],
        'Previous position': ['Previous position', 'Previous Position', 'Previous Rank', 'previous_position', 'Prev Position'],
        'Search Volume': ['Search Volume', 'search volume', 'Volume', 'volume', 'SV', 'Monthly Searches'],
        'Keyword Difficulty': ['Keyword Difficulty', 'keyword difficulty', 'Difficulty', 'KD', 'Competition Score'],
        'CPC': ['CPC', 'cpc', 'Cost Per Click', 'Cost per click', 'Avg CPC'],
        'URL': ['URL', 'url', 'Landing Page', 'landing page', 'Page URL'],
        'Traffic': ['Traffic', 'traffic', 'Est Traffic', 'Estimated Traffic', 'Organic Traffic'],
        'Traffic (%)': ['Traffic (%)', 'Traffic %', 'traffic_percent', 'Traffic Share', 'Share'],
        'Traffic Cost': ['Traffic Cost', 'traffic cost', 'Est Cost', 'Estimated Cost', 'Value'],
        'Competition': ['Competition', 'competition', 'Competitive Density', 'Density'],
        'Number of Results': ['Number of Results', 'Results', 'number_of_results', 'Total Results'],
        'Trends': ['Trends', 'trends', 'Trend', 'trend', 'Search Trend'],
        'Timestamp': ['Timestamp', 'timestamp', 'Date', 'date', 'Last Updated'],
        'SERP Features by Keyword': ['SERP Features by Keyword', 'SERP Features', 'serp_features', 'Features'],
        'Keyword Intents': ['Keyword Intents', 'Intent', 'intent', 'Search Intent', 'User Intent'],
        'Position Type': ['Position Type', 'Type', 'position_type', 'Result Type', 'SERP Type']
    }
    
    @staticmethod
    def load_file(file) -> Optional[pd.DataFrame]:
        """Load and validate CSV/Excel file with flexible column mapping."""
        try:
            if file is None:
                return None
                
            # Determine file type and load accordingly
            if file.name.endswith('.csv'):
                df = pd.read_csv(file, on_bad_lines='skip', engine='python')
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                st.error("Unsupported file format. Please use CSV or Excel files.")
                return None
            
            # Map columns to standard names
            df = DataLoader._map_columns(df)
            
            # Validate we have the required columns
            missing_cols = []
            for standard_col in DataLoader.COLUMN_MAPPING.keys():
                if standard_col not in df.columns:
                    missing_cols.append(standard_col)
            
            if missing_cols:
                st.error(f"Missing required columns: {missing_cols}")
                st.info("Please ensure your file contains columns for: " + ", ".join(missing_cols))
                return None
                
            # Clean and preprocess data
            df = DataLoader._clean_data(df)
            return df
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.info("Please check your file format and ensure it contains the required columns.")
            return None
    
    @staticmethod
    def _map_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Map flexible column names to standard names."""
        df = df.copy()
        column_mapping = {}
        
        for standard_name, possible_names in DataLoader.COLUMN_MAPPING.items():
            for col in df.columns:
                if col.strip().lower() in [name.lower() for name in possible_names]:
                    column_mapping[col] = standard_name
                    break
        
        return df.rename(columns=column_mapping)
    
    @staticmethod
    def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data."""
        # Create a copy to avoid modifying original
        df = df.copy()
        
        # Convert numeric columns
        numeric_cols = [
            'Position', 'Previous position', 'Search Volume', 
            'Keyword Difficulty', 'CPC', 'Traffic', 'Traffic (%)', 
            'Traffic Cost', 'Competition', 'Number of Results'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill NaN values
        df['Previous position'] = df['Previous position'].fillna(df['Position'])
        df['Keyword Difficulty'] = df['Keyword Difficulty'].fillna(50)
        df['CPC'] = df['CPC'].fillna(0)
        
        # Create additional calculated fields
        df['Position Change'] = df['Previous position'] - df['Position']
        df['Opportunity Score'] = (
            df['Search Volume'] * df['Traffic (%)']
        ) / (df['Keyword Difficulty'] + 1)
        df['Competitive Threat'] = df['Position'] * df['Traffic Cost']
        
        return df
    
    @staticmethod
    def validate_files(client_df: pd.DataFrame, competitor_df: pd.DataFrame) -> bool:
        """Validate that both files are properly loaded."""
        if client_df is None or competitor_df is None:
            return False
            
        if client_df.empty or competitor_df.empty:
            st.error("One or both files are empty")
            return False
            
        return True
    
    @staticmethod
    def get_sample_columns() -> dict:
        """Return sample column names for reference."""
        return {
            "Required Columns": list(DataLoader.COLUMN_MAPPING.keys()),
            "Flexible Names": {k: v[:3] for k, v in DataLoader.COLUMN_MAPPING.items()}
        }
