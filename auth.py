import dropbox
import os
from dropbox import DropboxOAuth2FlowNoRedirect
from dotenv import load_dotenv

# Load variables from your local .env file
load_dotenv()

# Configuration - Fetches from your .env file
APP_KEY = os.environ.get('DROPBOX_APP_KEY')
APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')

if not APP_KEY or not APP_SECRET:
    print("Error: APP_KEY or APP_SECRET not found in environment or .env file.")
    exit()

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')

authorize_url = auth_flow.start()
print("1. Go to this URL: " + authorize_url)
print("2. Click 'Allow'.")
print("3. Copy the authorization code provided by Dropbox.")

auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
    print("\n--- SUCCESS ---")
    print("Your Refresh Token is:", oauth_result.refresh_token)
    print("\nAdd this token to your .env file as: DROPBOX_REFRESH_TOKEN")
except Exception as e:
    print(f"Error during authorization: {e}")
