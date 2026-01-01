"""
Quick launcher for the Streamlit web UI
Run this file to start the web interface
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("Streamlit is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas"])
    
    # Run streamlit
    script_dir = os.path.dirname(os.path.abspath(__file__))
    web_app_path = os.path.join(script_dir, "web_app.py")
    
    print("Starting B2B Lead Discovery Web UI...")
    print("The web interface will open in your browser automatically.")
    print("Press Ctrl+C to stop the server.")
    
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", web_app_path,
        "--server.headless", "false",
        "--browser.gatherUsageStats", "false"
    ])

