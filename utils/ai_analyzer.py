import openai
import anthropic
import google.generativeai as genai
import streamlit as st
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
        
        # OpenAI - Use the correct method based on version
        openai_key = api_keys.get("openai_api_key", "")
        if openai_key and openai_key.strip():
            try:
                openai.api_key = openai_key
                self.openai_client = True
            except Exception as e:
                st.warning(f"OpenAI initialization failed: {str(e)}")
                self.openai_client = False
        else:
            self.openai_client = False
        
        # Anthropic - Safe initialization
        anthropic_key = api_keys.get("anthropic_api_key", "")
        if anthropic_key and anthropic_key.strip():
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            except Exception as e:
                st.warning(f"Anthropic initialization failed: {str(e)}")
                self.anthropic_client = None
        else:
            self.anthropic_client = None
        
        # Gemini - Safe initialization
        gemini_key = api_keys.get("gemini_api_key", "")
        if gemini_key and gemini_key.strip():
            try:
                genai.configure(api_key=gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                st.warning(f"Gemini initialization failed: {str(e)}")
                self.gemini_model = None
        else:
            self.gemini_model = None
    
    def generate_insights(self, analysis_data: Dict[str, Any], 
                         model: str = "openai") -> str:
        """Generate strategic insights using specified AI model."""
        
        prompt = self._build_analysis_prompt(analysis_data)
        
        try:
            if model == "openai" and self.openai_client:
                return self._openai_analysis(prompt)
            elif model == "anthropic" and self.anthropic_client:
                return self._anthropic_analysis(prompt)
            elif model == "gemini" and self.gemini_model:
                return self._gemini_analysis(prompt)
            else:
                return "AI analysis unavailable - API key not configured"
                
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def _build_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Build comprehensive prompt for AI analysis."""
        
        prompt = f"""
        You are an expert SEO strategist conducting a comprehensive keyword gap analysis.
        
        Based on the following data, provide strategic insights and actionable recommendations:
        
        CLIENT OVERVIEW:
        - Total Keywords: {data.get('client_total_keywords', 0)}
        - Average Position: {data.get('client_avg_position', 0):.2f}
        - Total Traffic: {data.get('client_total_traffic', 0):,.0f}
        - Traffic Cost: ${data.get('client_traffic_cost', 0):,.2f}
        
        COMPETITOR OVERVIEW:
        - Total Keywords: {data.get('competitor_total_keywords', 0)}
        - Average Position: {data.get('competitor_avg_position', 0):.2f}
        - Total Traffic: {data.get('competitor_total_traffic', 0):,.0f}
        - Traffic Cost: ${data.get('competitor_traffic_cost', 0):,.2f}
        
        KEY OPPORTUNITIES:
        Quick Wins (Client ranks 6-10, competitor ranks 1-5): {len(data.get('quick_wins', []))}
        Steal Opportunities (Client ranks 11+ or absent): {len(data.get('steal_opportunities', []))}
        Defensive Keywords (Client ranks 1-5, competitor gaining): {len(data.get('defensive_keywords', []))}
        
        TOP KEYWORDS BY CATEGORY:
        {self._format_keyword_lists(data)}
        
        Provide:
        1. Executive summary with key findings
        2. Immediate action items (next 30 days)
        3. Medium-term strategy (next 3 months)
        4. Long-term investment opportunities
        5. Content calendar recommendations
        6. Technical SEO priorities
        
        Focus on actionable insights that will drive organic visibility improvements.
        """
        
        return prompt
    
    def _format_keyword_lists(self, data: Dict[str, Any]) -> str:
        """Format keyword lists for the prompt."""
        formatted = ""
        
        for category, keywords in data.items():
            if isinstance(keywords, list) and keywords and isinstance(keywords[0], dict):
                formatted += f"\n{category.upper().replace('_', ' ')}:\n"
                for kw in keywords[:5]:  # Top 5 per category
                    formatted += f"- {kw.get('Keyword', 'N/A')} (Volume: {kw.get('Search Volume', 0):,}, Difficulty: {kw.get('Keyword Difficulty', 0)})\n"
        
        return formatted
    
    def _openai_analysis(self, prompt: str) -> str:
        """Generate analysis using OpenAI."""
        try:
            # Try the new method first
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert SEO strategist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback to older method
            try:
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
            except Exception as e2:
                return f"OpenAI API error: {str(e2)}"
    
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
            return self.openai_client
        elif model == "anthropic":
            return self.anthropic_client is not None
        elif model == "gemini":
            return self.gemini_model is not None
        return False
