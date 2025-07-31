# 🔎 AI Web Scraper

A modern, AI-powered web scraping tool that extracts specific information from any website using intelligent parsing.

## ✨ Features

- **🌐 Smart Web Scraping** - Fast, headless browser scraping
- **🤖 AI-Powered Parsing** - Extract specific data using local LLM (Ollama)
- **🎨 Modern UI** - Beautiful dark theme with gradient accents
- **⚡ Ultra-Fast** - Optimized for speed and efficiency
- **📊 Structured Output** - Clean, formatted results
- **🛠️ Easy Setup** - Simple installation and configuration

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
3. **Chrome/Chromium** browser installed

### Installation

1. **Clone or download** this project
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test installation:**
   ```bash
   python test_imports.py
   ```

4. **Start Ollama** (if not running):
   ```bash
   ollama serve
   ```

5. **Pull the AI model:**
   ```bash
   ollama pull llama3
   ```

### Running the App

```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`

## 📖 Usage Guide

### 1. Enter Website URL
- Paste any website URL you want to scrape
- Click "🕷️ Scrape Website"

### 2. Describe What to Extract
- In the parsing section, describe what information you want
- Examples:
  - "Extract all project names and technologies"
  - "Get all product prices and names"
  - "Find contact information and addresses"

### 3. Parse Content
- Click "🚀 Parse Content"
- AI will extract the requested information
- Results appear in a clean, formatted table

## ⚙️ Settings

### Sidebar Options:
- **Headless Mode** - Faster scraping (recommended ON)
- **Page Load Wait Time** - How long to wait for page loading
- **AI Model** - Choose between llama3, gpt-4, mistral
- **Max Chunk Size** - Size of content chunks for processing

## 🔧 Configuration

### Environment Variables
Create a `.env` file for custom settings:
```env
OLLAMA_BASE_URL=http://localhost:11434
CHROME_DRIVER_PATH=./chromedriver.exe
```

### Model Configuration
The AI model can be configured in `parse.py`:
```python
model = OllamaLLM(
    model="llama3",
    temperature=0.0,
    max_tokens=80,
    timeout=8
)
```

## 🛠️ Troubleshooting

### Common Issues:

1. **"Chrome driver not found"**
   - Download chromedriver.exe for your Chrome version
   - Place it in the project root directory

2. **"Ollama connection failed"**
   - Ensure Ollama is running: `ollama serve`
   - Check if model is pulled: `ollama list`

3. **"Import errors"**
   - Run: `pip install -r requirements.txt`
   - Test with: `python test_imports.py`

4. **"Slow parsing"**
   - Reduce chunk size in settings
   - Use smaller content sections
   - Check Ollama model performance

### Performance Tips:

- ✅ Keep headless mode ON
- ✅ Use smaller chunk sizes for better parsing
- ✅ Be specific in extraction requests
- ✅ Try different AI models for better results

## 📁 Project Structure

```
AI Web Scraper/
├── main.py              # Main Streamlit application
├── scrape.py            # Web scraping functions
├── parse.py             # AI parsing functions
├── requirements.txt     # Python dependencies
├── test_imports.py     # Dependency testing
├── chromedriver.exe    # Chrome driver
└── README.md           # This file
```

## 🔄 Updates

### Recent Improvements:
- ✅ **Ultra-fast parsing** - Single chunk processing
- ✅ **Structured data** - Preserves HTML structure
- ✅ **Clean output** - No verbose explanations
- ✅ **Better error handling** - Comprehensive fallbacks
- ✅ **Modern UI** - Dark theme with gradients

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Run `python test_imports.py`
3. Ensure all dependencies are installed
4. Verify Ollama is running

---

**Made with ❤️ using Streamlit | AI Web Scraper v1.0** 