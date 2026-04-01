import dropbox
import markdown
import os
import time
import logging

# Security: Fetches credentials from environment variables
APP_KEY = os.environ.get('DROPBOX_APP_KEY')
APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')
REFRESH_TOKEN = os.environ.get('DROPBOX_REFRESH_TOKEN')
OUTPUT_DIR = 'web_output'
SYNC_INTERVAL = 60 

logging.basicConfig(level=logging.INFO)

def sync_and_render():
    if not all([APP_KEY, APP_SECRET, REFRESH_TOKEN]):
        logging.error("Missing environment variables. Ensure APP_KEY, APP_SECRET, and REFRESH_TOKEN are set.")
        return

    dbx = dropbox.Dropbox(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        oauth2_refresh_token=REFRESH_TOKEN
    )
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        res = dbx.files_list_folder('')
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.lower().endswith('.md'):
                metadata, response = dbx.files_download(entry.path_lower)
                md_content = response.content.decode('utf-8')
                html_body = markdown.markdown(md_content)
                
                full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{entry.name.replace('.md', '')}</title>
    <style>
        body {{ font-family: -apple-system, system-ui, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #24292e; }}
        pre {{ background: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; }}
        code {{ background: #afb8c133; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
    </style>
</head>
<body>{html_body}</body>
</html>"""
                
                file_name = os.path.splitext(entry.name)[0] + '.html'
                with open(os.path.join(OUTPUT_DIR, file_name), 'w', encoding='utf-8') as f:
                    f.write(full_html)
                logging.info(f"Updated: {file_name}")

    except Exception as e:
        logging.error(f"Sync failed: {e}")

if __name__ == "__main__":
    while True:
        sync_and_render()
        time.sleep(SYNC_INTERVAL)
