import pandas as pd
import streamlit as st
from typing import Optional


class DataLoader:
    """Handles loading and validation of CSV files for keyword analysis."""
    
    REQUIRED_COLUMNS = [
        'Keyword', 'Position', 'Previous position', 'Search Volume', 
        'Keyword Difficulty', 'CPC', 'URL', 'Traffic', 'Traffic (%)', 
        'Traffic Cost', 'Competition', 'Number of Results', 'Trends', 
        'Timestamp', 'SERP Features by Keyword', 'Keyword Intents', 'Position Type'
    ]
    
    @staticmethod
    def load_file(file) -> Optional[pd.DataFrame]:
        """Load and validate CSV/Excel file."""
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
            
            # Validate required columns
            missing_cols = set(DataLoader.REQUIRED_COLUMNS) - set(df.columns)
            if missing_cols:
                st.error(f"Missing required columns: {missing_cols}")
                return None
                
            # Clean and preprocess data
            df = DataLoader._clean_data(df)
            return df
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None
    
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
