import pandas as pd
import streamlit as st
from typing import Optional


class DataLoader:
    """Handles loading and validation of CSV files for keyword analysis."""
    
    # Standard required columns
    REQUIRED_COLUMNS = [
        'Keyword', 'Position', 'Previous position', 'Search Volume',
        'Keyword Difficulty', 'CPC', 'URL', 'Traffic', 'Traffic (%)',
        'Traffic Cost', 'Competition', 'Number of Results', 'Trends',
        'Timestamp', 'SERP Features by Keyword', 'Keyword Intents', 'Position Type'
    ]
    
    @staticmethod
    def load_file(file) -> Optional[pd.DataFrame]:
        """Load and validate CSV/Excel file with automatic delimiter detection."""
        try:
            if file is None:
                return None
                
            # Load file with automatic delimiter detection
            if file.name.endswith('.csv'):
                # Try to detect delimiter
                import io
                content = file.read().decode('utf-8')
                file.seek(0)  # Reset file pointer
                
                # Check first line for delimiter
                first_line = content.split('\n')[0]
                delimiter = ';' if ';' in first_line else ','
                
                df = pd.read_csv(file, sep=delimiter, on_bad_lines='skip', engine='python')
                
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                st.error("Unsupported file format. Please use CSV or Excel files.")
                return None
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Show detected columns for debugging
            st.write("✅ **File loaded successfully!**")
            st.write("Detected columns:", list(df.columns))
            
            # Check if we have the exact columns needed
            exact_match = all(col in df.columns for col in DataLoader.REQUIRED_COLUMNS)
            
            if exact_match:
                st.success("✅ All required columns found!")
                df = DataLoader._clean_data(df)
                return df
            
            # Try to map columns if exact match fails
            st.info("🔍 Attempting column mapping...")
            df = DataLoader._map_columns(df)
            
            # Check again
            missing_cols = [col for col in DataLoader.REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                st.error(f"❌ Missing columns: {missing_cols}")
                
                # Show what's available
                st.write("Available columns:", list(df.columns))
                
                # Create template
                template = DataLoader.create_template()
                st.write("📋 **Template with exact column names:**")
                st.dataframe(template.head(1))
                
                # Provide download
                csv = template.to_csv(index=False)
                st.download_button(
                    label="📥 Download Template CSV",
                    data=csv,
                    file_name="keyword_gap_template.csv",
                    mime="text/csv"
                )
                
                return None
            
            # Clean and preprocess data
            df = DataLoader._clean_data(df)
            return df
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("💡 **Tip:** Make sure your CSV uses either commas (,) or semicolons (;) as delimiters.")
            return None
    
    @staticmethod
    def _map_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Map columns to standard names."""
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Direct mapping (case-insensitive)
        column_mapping = {}
        for col in df.columns:
            for standard in DataLoader.REQUIRED_COLUMNS:
                if col.lower() == standard.lower():
                    column_mapping[col] = standard
                    break
        
        return df.rename(columns=column_mapping)
    
    @staticmethod
    def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data."""
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
        
        # Create calculated fields
        df['Position Change'] = df['Previous position'] - df['Position']
        df['Opportunity Score'] = (
            df['Search Volume'] * df['Traffic (%)']
        ) / (df['Keyword Difficulty'] + 1)
        
        return df
    
    @staticmethod
    def create_template():
        """Create a template CSV with all required columns."""
        template = pd.DataFrame(columns=DataLoader.REQUIRED_COLUMNS)
        template.loc[0] = [
            'example keyword', 1, 2, 1000, 45, 2.5, 'https://example.com', 800, 80.0,
            2000.0, 0.8, 500000, 0.15, '2024-07-25', 'Featured snippet', 'Commercial', 'Regular'
        ]
        return template
    
    @staticmethod
    def validate_columns(df):
        """Check which columns are present."""
        return {
            'present': [col for col in DataLoader.REQUIRED_COLUMNS if col in df.columns],
            'missing': [col for col in DataLoader.REQUIRED_COLUMNS if col not in df.columns],
            'available': list(df.columns)
        }
