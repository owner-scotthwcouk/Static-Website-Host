# Static Website Host

An automated tool that transforms Markdown files in a specific Dropbox App folder into a static website.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set Environment Variables or update `main.py` with your Dropbox App Key, Secret, and Refresh Token.
3. Run the script: `python main.py`
4. Serve the output: `python -m http.server 8000 --directory web_output`