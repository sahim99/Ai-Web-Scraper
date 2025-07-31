import sys
import subprocess

def test_imports():
    """Test all required imports"""
    required_packages = [
        'streamlit',
        'langchain',
        'langchain_ollama', 
        'selenium',
        'bs4',
        'lxml',
        'html5lib',
        'dotenv',
        're',
        'time',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'bs4':
                import bs4
            elif package == 're':
                import re
            elif package == 'time':
                import time
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True

def test_functionality():
    """Test basic functionality"""
    try:
        # Test scraping
        from scrape import scrape_website, clean_body_content
        print("✅ Scraping functions imported")
        
        # Test parsing
        from parse import perse_with_Ollama
        print("✅ Parsing functions imported")
        
        # Test main app
        import streamlit as st
        print("✅ Streamlit imported")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing AI Web Scraper Dependencies...\n")
    
    imports_ok = test_imports()
    print("\n" + "="*50 + "\n")
    
    if imports_ok:
        functionality_ok = test_functionality()
        if functionality_ok:
            print("\n🎉 All tests passed! Your AI Web Scraper is ready to use.")
        else:
            print("\n⚠️ Some functionality tests failed. Check your setup.")
    else:
        print("\n❌ Please install missing packages first.")
