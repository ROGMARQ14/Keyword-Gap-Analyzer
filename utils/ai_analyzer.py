import openai
import anthropic
import google.generativeai as genai
import streamlit as st
import pandas as pd
from typing import Dict, Any
import toml

class AIAnalyzer:
    """Handles AI-powered analysis using OpenAI, Anthropic, and Gemini APIs."""
    
    def __init__(self):
        self.config = self._load_config()
        self._setup_clients()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from TOML files."""
        try:
            with open('config.toml', 'r') as f:
                return toml.load(f)
        except FileNotFoundError:
            return {}
    
    def _setup_clients(self):
        """Initialize AI clients with API keys."""
        # Try Streamlit secrets first, then config file
        api_keys = st.secrets.get("api_keys", {})
        if not api_keys:
            api_keys = self.config.get("api_keys", {})
        
        # OpenAI
        openai_key = api_keys.get("openai_api_key", "")
        if openai_key:
            openai.api_key = openai_key
        
        # Anthropic
        anthropic_key = api_keys.get("anthropic_api_key", "")
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        else:
            self.anthropic_client = None
        
        # Gemini
        gemini_key = api_keys.get("gemini_api_key", "")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini_model = None
    
    def generate_insights(self, analysis_data: Dict[str, Any], 
                         model: str = "openai") -> str:
        """Generate strategic insights using selected AI model."""
        
        prompt = self._create_analysis_prompt(analysis_data)
        
        try:
            if model == "openai" and openai.api_key:
                return self._openai_analysis(prompt)
            elif model == "anthropic" and self.anthropic_client:
                return self._anthropic_analysis(prompt)
            elif model == "gemini" and self.gemini_model:
                return self._gemini_analysis(prompt)
            else:
                return "AI model not configured or available."
                
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create comprehensive analysis prompt."""
        
        prompt = f"""
        You are an expert SEO strategist analyzing keyword gap data. 
        
        CLIENT PERFORMANCE:
        - Total Keywords: {data['client_total_keywords']:,}
        - Average Position: {data['client_avg_position']:.1f}
        - Total Traffic: {data['client_total_traffic']:,}
        - Traffic Value: ${data['client_traffic_cost']:,}
        
        COMPETITOR PERFORMANCE:
        - Total Keywords: {data['competitor_total_keywords']:,}
        - Average Position: {data['competitor_avg_position']:.1f}
        - Total Traffic: {data['competitor_total_traffic']:,}
        - Traffic Value: ${data['competitor_traffic_cost']:,}
        
        QUICK WINS (Client ranks 6-10, Competitor ranks 1-5):
        {len(data['quick_wins'])} opportunities identified
        
        STEAL OPPORTUNITIES (Competitor ranks 1-5, Client absent/poor):
        {len(data['steal_opportunities'])} opportunities identified
        
        DEFENSIVE KEYWORDS (Client ranks 1-5, Competitor close):
        {len(data['defensive_keywords'])} keywords to defend
        
        Provide a comprehensive strategic analysis including:
        
        1. **Executive Summary** - Key insights and market position
        2. **Immediate Actions** - Top 5 priorities for next 30 days
        3. **Medium-term Strategy** - 3-month content and optimization plan
        4. **Long-term Investment** - 6-12 month strategic initiatives
        5. **Resource Allocation** - Budget and team recommendations
        6. **Risk Assessment** - Competitive threats and mitigation strategies
        
        Format as a professional report with clear sections and actionable recommendations.
        """
        
        return prompt
    
    def _openai_analysis(self, prompt: str) -> str:
        """Generate analysis using OpenAI GPT-4."""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert SEO strategist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def _anthropic_analysis(self, prompt: str) -> str:
        """Generate analysis using Anthropic Claude."""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _gemini_analysis(self, prompt: str) -> str:
        """Generate analysis using Google Gemini."""
        response = self.gemini_model.generate_content(prompt)
        return response.text
    
    def is_configured(self, model: str) -> bool:
        """Check if specified model is configured."""
        if model == "openai":
            return bool(openai.api_key)
        elif model == "anthropic":
            return self.anthropic_client is not None
        elif model == "gemini":
            return self.gemini_model is not None
        return False
