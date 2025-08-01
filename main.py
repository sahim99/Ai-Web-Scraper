

import streamlit as st
import time
from scrape import scrape_website, extract_body_content, clean_body_content

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Web Scraper",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR MODERN DESIGN ---
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        font-weight: 400;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        color: white;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: rgba(255,255,255,0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        color: white;
        padding: 0.75rem;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div > div {
        background: rgba(255,255,255,0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    /* Toggle styling */
    .stToggle > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metric styling */
    .metric-container {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Card styling */
    .card {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Section headers */
    .section-header {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header-container">
    <div class="header-title">🔎 AI Web Scraper</div>
    <div class="header-subtitle">Extract specific information from any website using AI-powered parsing</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR (SETTINGS) ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    headless = st.toggle("Headless Mode", value=True)
    wait_time = st.slider("Page Load Wait Time (seconds)", 1, 5, 2)
    ai_model = st.selectbox("AI Model", ["llama3", "gpt-4", "mistral"])
    chunk_size = st.slider("Max Chunk Size", 2000, 5000, 4000, step=500)
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div style="font-size: 0.9rem; color: #667eea;">Websites Scraped</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: white;">1</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div style="font-size: 0.9rem; color: #667eea;">Content Parsed</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: white;">0</div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN CONTENT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">🌐 Enter Website URL</div>', unsafe_allow_html=True)
    
    url = st.text_input("Website URL", placeholder="https://example.com")
    
    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        scrape_btn = st.button("🕷️ Scrape Website", use_container_width=True)
    with col_btn2:
        reset_btn = st.button("🔄 Reset", use_container_width=True)
    
    # Reset functionality
    if reset_btn:
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("✅ Reset complete!")
        st.rerun()
    
    # Scraping functionality
    if scrape_btn and url:
        with st.spinner("🕷️ Scraping website..."):
            try:
                result = scrape_website(url)
                if result:
                    body_content = extract_body_content(result)
                    cleaned_content = clean_body_content(body_content)
                    st.session_state.dom_content = cleaned_content
                    st.session_state.current_url = url
                    
                    # Show success message
                    st.success(f"✅ Website scraped successfully! Content length: {len(cleaned_content)} characters")
                    
                    with st.expander("📄 View DOM Content", expanded=False):
                        st.text_area("DOM Content", cleaned_content, height=300)
                else:
                    st.error("❌ Failed to scrape website")
            except Exception as e:
                st.error(f"❌ Error scraping website: {str(e)}")
    
    # Parsing functionality
    if "dom_content" in st.session_state:
        st.markdown('<div class="section-header">🤖 Parse Content</div>', unsafe_allow_html=True)
        
        # Parse input
        parse_description = st.text_area("Describe what you want to parse from the scraped content")
        
        # Action buttons
        col_parse, col_copy, col_clear = st.columns(3)
        with col_parse:
            parse_btn = st.button("🚀 Parse Content", use_container_width=True)
        with col_copy:
            copy_btn = st.button("📋 Copy Results", use_container_width=True)
        with col_clear:
            clear_btn = st.button("🗑️ Clear Results", use_container_width=True)
        
        # Clear Results functionality
        if clear_btn:
            if "parsed_result" in st.session_state:
                del st.session_state.parsed_result
            if "current_query" in st.session_state:
                del st.session_state.current_query
            st.success("✅ Results cleared!")
            st.rerun()
        
        # Copy Results functionality
        if copy_btn and st.session_state.get("parsed_result"):
            st.code(st.session_state["parsed_result"], language=None)
            st.success("Content copied! (Select and copy manually)")
        
        # Parse functionality - PERFECTED LOGIC
        if parse_btn and parse_description:
            # Store current query
            st.session_state.current_query = parse_description
            # Set processing state
            st.session_state.is_processing = True
            
            # Create a progress bar for AI processing
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Update progress and status
            status_text.text("🤖 Initializing AI processing...")
            progress_bar.progress(25)
            
            status_text.text("🤖 Analyzing content structure...")
            progress_bar.progress(50)
            
            status_text.text("🤖 Extracting information with AI...")
            progress_bar.progress(75)
            
            try:
                from parse import perse_with_Ollama
                
                result = perse_with_Ollama(st.session_state.dom_content, parse_description)
                
                # Complete the progress bar
                status_text.text("🤖 Processing complete!")
                progress_bar.progress(100)
                
                # Store the result
                st.session_state.parsed_result = result
                
                if result and result.strip() and result != "No matching information found":
                    st.success("✅ Parsing complete!")
                else:
                    st.warning("⚠️ No matching information found")
                    st.info("💡 Try being more specific in your query. For example:")
                    st.code("""
• "Find information about the person named Sahim"
• "Extract personal details and background"
• "Get the name, skills, and experience"
• "List all projects with technologies"
                    """)
                    
            except Exception as e:
                st.error(f"❌ Error parsing content: {str(e)}")
                st.info("💡 Make sure Ollama is running: ollama serve")
            finally:
                # Clear progress bar and status
                progress_bar.empty()
                status_text.empty()
                # Clear processing state
                st.session_state.is_processing = False
        
        # Show results ONLY if we have valid parsed results
        if (parse_description and 
            "parsed_result" in st.session_state and 
            "current_query" in st.session_state and 
            st.session_state.current_query == parse_description):
            
            result = st.session_state.parsed_result
            
            # Only show card if result is valid and not empty
            if (result and 
                isinstance(result, str) and
                result.strip() and 
                result != "No matching information found" and
                len(result.strip()) > 10):
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📋 Parsed Results")
                st.write(result)
                st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Check if processing is running and apply dimming effect
    is_processing = st.session_state.get("is_processing", False)
    
    if is_processing:
        st.markdown('<div style="opacity: 0.4; pointer-events: none;">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">💡 Quick Examples</div>', unsafe_allow_html=True)
    
    if st.button("📰 News Website", use_container_width=True, disabled=is_processing):
        st.info("Try scraping a news website like CNN, BBC, or Reuters")
    
    if st.button("🛒 E-commerce Site", use_container_width=True, disabled=is_processing):
        st.info("Try scraping product information from Amazon, eBay, or Shopify stores")
    
    if st.button("🏢 Company Website", use_container_width=True, disabled=is_processing):
        st.info("Try scraping company information, contact details, or services")
    
    st.markdown("---")
    st.markdown('<div class="section-header">⚡ Quick Tips</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <ul style="color: white; margin: 0; padding-left: 1.5rem;">
            <li>Keep headless mode ON for faster scraping</li>
            <li>Use smaller chunk sizes for better parsing</li>
            <li>Be specific in your extraction requests</li>
            <li>Try different AI models for better results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if is_processing:
        st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #667eea; padding: 2rem;'>"
    "Made with ❤️ using Streamlit | AI Web Scraper v1.0"
    "</div>",
    unsafe_allow_html=True
)
        
    


