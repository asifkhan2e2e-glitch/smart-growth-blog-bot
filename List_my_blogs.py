"""
Ye script blogger_auth.py chalane ke BAAD chalani hai.
Kaam: aapke account ke saare Blogger blogs aur unke IDs dikhayega.
Wahi Blog ID hume publishing ke liye chahiye hogi.

Chalane ka tareeqa:
    python list_my_blogs.py
"""

import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = "token_blogger.json"


def main():
    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"],
    )

    service = build("blogger", "v3", credentials=creds)
    blogs = service.blogs().listByUser(userId="self").execute()

    print("\nAapke Blogger blogs:\n")
    for blog in blogs.get("items", []):
        print(f"Naam: {blog['name']}")
        print(f"URL:  {blog['url']}")
        print(f"Blog ID: {blog['id']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
