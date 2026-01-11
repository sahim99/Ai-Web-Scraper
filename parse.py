from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Perfect template for all query types
template = (
    "Content: {dom_content}\n\n"
    "Query: {parse_description}\n\n"
    "Instructions:\n"
    "1. Answer ONLY what is specifically asked for\n"
    "2. If asking about a person, provide their background, skills, experience\n"
    "3. If asking about projects, create a table with Project | Technology format\n"
    "4. If asking about products, list features and specifications\n"
    "5. If asking about skills/technologies, list them clearly\n"
    "6. If the specific thing asked for is NOT found, return 'No matching information found'\n"
    "7. Keep answers concise and well-organized\n"
    "8. Use tables when appropriate for structured data"
)

# Optimized model configuration
model = OllamaLLM(
    model="llama3",
    temperature=0.0,
    max_tokens=300,
    timeout=20
)

def perse_with_Ollama(dom_content, parse_description):
    """Perfect parser that handles all query types accurately"""
    
    if not dom_content or not parse_description:
        return "No content to parse"
    
    try:
        # Use optimal content length
        content = dom_content[:4000]
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        
        response = chain.invoke({
            "dom_content": content,
            "parse_description": parse_description
        })
        
        # Get result
        if hasattr(response, 'content'):
            result = response.content
        else:
            result = str(response)
        
        # Perfect cleaning logic
        if result and result.strip():
            clean_result = result.strip()
            
            # Remove verbose prefixes but keep actual content
            verbose_prefixes = [
                "Here is the extracted information:",
                "Here's the extracted information:",
                "Based on the content:",
                "The answer to your question is:",
                "According to the provided content:"
            ]
            
            for prefix in verbose_prefixes:
                if clean_result.startswith(prefix):
                    clean_result = clean_result[len(prefix):].strip()
                    break
            
            # Remove trailing explanations
            if "Let me know" in clean_result:
                clean_result = clean_result.split("Let me know")[0]
            if "Note:" in clean_result:
                clean_result = clean_result.split("Note:")[0]
            
            final_result = clean_result.strip()
            
            # Return only if meaningful
            if len(final_result) > 10:
                return final_result
            else:
                return "No matching information found"
        else:
            return "No matching information found"
            
    except Exception as e:
        # Better error handling
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            return "Error: Request timed out. Please try again."
        elif "connection" in error_msg.lower():
            return "Error: Connection failed. Make sure Ollama is running."
        else:
            return f"Error: {error_msg}"


def parse_with_groq(dom_content, parse_description):
    """Parse content using Groq's ultra-fast API"""
    import os
    import requests
    import json
    
    # You can hardcode your key here for testing, or set it in environment variables
    # api_key = "gsk_..." 
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return "Error: GROQ_API_KEY not found. Please set your API key in environment variables or hardcode it in parse.py"
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Use optimal content length for Llama 3 on Groq (8k context usually)
    content = dom_content[:6000]
    
    prompt = template.format(dom_content=content, parse_description=parse_description)
    
    payload = {
        "model": "llama-3.3-70b-versatile", # Updated to latest supported model
        "messages": [
            {"role": "system", "content": "You are a helpful web scraping assistant. Extract information precisely."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return content.strip()
            else:
                return "Error: Empty response from Groq"
        else:
            return f"Error: Groq API returned status code {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}"
