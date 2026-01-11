![AI Web Scraper UI](./image.png)

# 🔎 AI Web Scraper

A modern, high-performance web scraping tool that combines **Selenium** for robust browsing and **AI (LLMs)** for intelligent data extraction. 

Currently configured to use **Groq Cloud API** (Llama 3.3) for ultra-fast, free, and lightweight parsing on your local machine.

## ✨ Features

- **⚡ Blazing Fast AI** - Uses Groq's LPU inference engine (Llama 3.3-70b)
- **🌐 Smart Scraping** - Headless Selenium browser handles dynamic JS-heavy websites
- **🎨 Modern UI** - Beautiful Dark Mode Streamlit interface with real-time feedback
- **📊 Structured Data** - Extracts clean tables, lists, and summaries from raw HTML
- **🛡️ Robust Cleaning** - Smart content filtering to remove noise (scripts, styles, ads)

---

## 🚀 Quick Start

### Prerequisites

1.  **Python 3.8+** installed
2.  **Google Chrome** installed
3.  **Groq API Key** (Free) - Get one at [console.groq.com](https://console.groq.com/keys)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ai-web-scraper
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

1.  **Start the application:**
    ```bash
    streamlit run main.py
    ```
    
2.  **Open in Browser:**
    Go to `http://localhost:8501`

---

## 📖 How It Works

1.  **Scraping Layer (`scrape.py`)**: 
    - Launches a headless Chrome browser
    - Navigates to the URL and bypasses basic protections
    - Cleans the DOM to preserve only visible text content

2.  **Intelligence Layer (`parse.py`)**:
    - The cleaned text is sent to the **Groq Cloud API**
    - **Llama 3.3-70b** processes the content using specific user instructions
    - Returns structured, precise answers

3.  **UI Layer (`main.py`)**:
    - A responsive Streamlit dashboard manages the workflow
    - Visual progress bars and status updates keep you informed

---

## ⚙️ Configuration

### Switching to Offline Mode (Ollama)
If you prefer total privacy and offline usage:
1.  Install [Ollama](https://ollama.com) and run `ollama serve`
2.  Open `main.py`
3.  Comment out the Groq import and uncomment Ollama:
    ```python
    # from parse import parse_with_groq 
    from parse import perse_with_Ollama  # Use this for local
    ```

### Environment Variables
- `GROQ_API_KEY`: Automatically handled by the app (via `setx` or fallback)
- `CHROME_DRIVER_PATH`: Managed automatically by `webdriver-manager`

---

## 🛠️ Troubleshooting

- **"Module not found" error**: Run `python -m pip install -r requirements.txt`
- **"Chrome session not created"**: The app auto-updates the driver, but try updating your Chrome browser if issues persist.
- **"Empty results"**: Try being more specific in your query (e.g., "List all projects" instead of just "projects").

---

**Made with ❤️ using Streamlit & Groq**
