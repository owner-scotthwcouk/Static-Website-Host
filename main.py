import dropbox
import markdown
import os

# Configuration
APP_KEY = 'd06mcqwavdik8b0'
APP_SECRET = 'nx82n75ppr9wb6w'
REFRESH_TOKEN = '0TRDii8DpSYAAAAAAAAAAXSfLvwHXNMfJGJ3UzFGCesTwRmCcO2msboXu8RpRdU1'
OUTPUT_DIR = 'web_output'

def sync_and_render():
    dbx = dropbox.Dropbox(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        oauth2_refresh_token=REFRESH_TOKEN
    )
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        # Check files in the App folder
        res = dbx.files_list_folder('')
        
        files_found = False
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.lower().endswith('.md'):
                files_found = True
                # Download
                metadata, response = dbx.files_download(entry.path_lower)
                md_content = response.content.decode('utf-8')
                
                # Convert
                html_body = markdown.markdown(md_content)
                
                full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{entry.name}</title>
    <style>
        body {{ 
            font-family: -apple-system, sans-serif; 
            line-height: 1.6; 
            max-width: 800px; 
            margin: 40px auto; 
            padding: 20px; 
            color: #24292e;
        }}
        pre {{ background: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; }}
        code {{ background: #afb8c133; padding: 2px 4px; border-radius: 4px; }}
    </style>
</head>
<body>{html_body}</body>
</html>"""
                
                file_name = os.path.splitext(entry.name)[0] + '.html'
                output_path = os.path.join(OUTPUT_DIR, file_name)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                
                print(f"Rendered: {file_name}")
        
        if not files_found:
            print("No .md files found in the Dropbox App folder.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_and_render()