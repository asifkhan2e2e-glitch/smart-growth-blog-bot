"""
Ye script SIRF EK BAAR chalani hai (pehli setup ke waqt).
Kaam: client_secret_blogger.json se browser me login karwayega,
phir ek token_blogger.json file save karega jo future me
dobara login kiye baghair Blogger API use karne dega.

Chalane ka tareeqa:
    python blogger_auth.py
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Ye scope Blogger par posts likhne/publish karne ki permission deta hai
SCOPES = ["https://www.googleapis.com/auth/blogger"]

CLIENT_SECRET_FILE = "client_secret_blogger.json"  # yahan apni downloaded file ka naam confirm kar lein
TOKEN_FILE = "token_blogger.json"


def main():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

    # Ye browser open karega, aap apne Google account se login/authorize karenge
    creds = flow.run_local_server(port=0)

    # Token save kar dete hain taake dobara login na karna pade
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }

    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

    print(f"\n✅ Authorization successful! Token saved to '{TOKEN_FILE}'.")
    print("Ab aap 'list_my_blogs.py' chala kar apna Blog ID nikal sakte hain.")


if __name__ == "__main__":
    main()
