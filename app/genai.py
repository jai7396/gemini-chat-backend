import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Make sure .env file is loaded properly.")

genai.configure(api_key=GOOGLE_API_KEY)

def list_available_models():
    """Helper function to list all available models"""
    try:
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
        return available_models
    except Exception as e:
        return f"Error listing models: {str(e)}"

def send_to_gemini(message: str) -> str:
    try:
        # Try the current model names in order of preference
        model_names = [
            "gemini-1.5-flash",     # Latest and fastest
            "gemini-1.5-pro",      # More capable but slower
            "gemini-1.0-pro",      # Fallback option
        ]
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(message)
                return response.text.strip()
            except Exception as model_error:
                print(f"Failed with {model_name}: {str(model_error)}")
                continue
        
        # If all models fail, return the available models for debugging
        available = list_available_models()
        return f"All models failed. Available models: {available}"
        
    except Exception as e:
        return f"Gemini error: {str(e)}"

# Optional: Function to get the best available model
def get_best_model():
    """Returns the best available model for your use case"""
    try:
        models = genai.list_models()
        # Priority order: flash > pro > fallbacks
        preferred_order = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
        
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name.split('/')[-1])  # Get just the model name
        
        for preferred in preferred_order:
            if preferred in available_models:
                return preferred
                
        # Return first available if none of the preferred ones work
        return available_models[0] if available_models else None
        
    except Exception:
        return "gemini-1.5-flash"  # Safe default