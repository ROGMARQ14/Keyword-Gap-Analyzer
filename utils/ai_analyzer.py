import openai
import anthropic
import google.generativeai as genai
import streamlit as st
from typing import Dict, Any, List
import toml

class AIAnalyzer:
    """Handles AI-powered analysis using OpenAI, Anthropic, and Gemini APIs."""
    
    def __init__(self):
        self.config = self._load_config()
        self._setup_clients()
        self._setup_models()
    
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
        
        # OpenAI - Use the new client
        openai_key = api_keys.get("openai_api_key", "")
        if openai_key and openai_key.strip():
            try:
                self.openai_client = openai.OpenAI(api_key=openai_key)
            except Exception as e:
                st.warning(f"OpenAI initialization failed: {str(e)}")
                self.openai_client = None
        else:
            self.openai_client = None
        
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
    
    def _setup_models(self):
        """Setup available models for each provider."""
        self.models = {
            "openai": [
                "gpt-4",
                "gpt-4-turbo",
                "gpt-3.5-turbo",
                "gpt-4o",
                "gpt-4o-mini"
            ],
            "anthropic": [
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229"
            ],
            "gemini": [
                "gemini-pro",
                "gemini-1.5-pro",
                "gemini-1.5-flash"
            ]
        }
    
    def get_available_models(self, provider: str) -> List[str]:
        """Get available models for a specific provider."""
        return self.models.get(provider, [])
    
    def is_provider_configured(self, provider: str) -> bool:
        """Check if a specific provider is configured."""
        if provider == "openai":
            return self.openai_client is not None
        elif provider == "anthropic":
            return self.anthropic_client is not None
        elif provider == "gemini":
            return self.gemini_model is not None
        return False
    
    def get_configured_providers(self) -> List[str]:
        """Get list of configured providers."""
        providers = []
        if self.openai_client:
            providers.append("openai")
        if self.anthropic_client:
            providers.append("anthropic")
        if self.gemini_model:
            providers.append("gemini")
        return providers
    
    def generate_insights(self, analysis_data: Dict[str, Any], 
                         provider: str, model: str) -> str:
        """Generate strategic insights using specified provider and model."""
        
        prompt = self._build_analysis_prompt(analysis_data)
        
        try:
            if provider == "openai" and self.openai_client:
                return self._openai_analysis(prompt, model)
            elif provider == "anthropic" and self.anthropic_client:
                return self._anthropic_analysis(prompt, model)
            elif provider == "gemini" and self.gemini_model:
                return self._gemini_analysis(prompt, model)
            else:
                return f"{provider} is not configured or model is not available"
                
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
    
    def _openai_analysis(self, prompt: str, model: str) -> str:
        """Generate analysis using OpenAI."""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO strategist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API error: {str(e)}"
    
    def _anthropic_analysis(self, prompt: str, model: str) -> str:
        """Generate analysis using Anthropic Claude."""
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=2000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Anthropic API error: {str(e)}"
    
    def _gemini_analysis(self, prompt: str, model: str) -> str:
        """Generate analysis using Google Gemini."""
        try:
            if model == "gemini-pro":
                response = self.gemini_model.generate_content(prompt)
            else:
                # Handle other Gemini models
                model_instance = genai.GenerativeModel(model)
                response = model_instance.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini API error: {str(e)}"
