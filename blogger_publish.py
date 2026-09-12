"""
Ye module saved token_blogger.json use kar ke Blogger par post publish karta hai.
Isay directly nahi chalana — ye 'main.py' ke andar use hota hai.
"""

import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_FILE = "token_blogger.json"

# Aapki Blog ID (Smart Growth: AI)
BLOG_ID = "7538643036301400495"


def load_token_data():
    """
    Local computer par: token_blogger.json file se padhta hai.
    GitHub Actions par: BLOGGER_TOKEN_JSON secret (environment variable) se padhta hai.
    """
    env_token = os.environ.get("BLOGGER_TOKEN_JSON")
    if env_token:
        return json.loads(env_token)

    with open(TOKEN_FILE, "r") as f:
        return json.load(f)


def get_blogger_service():
    token_data = load_token_data()

    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"],
    )

    # Agar token expire ho chuka ho to khud-ba-khud refresh kar leta hai
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_data["token"] = creds.token
        # Sirf local file wale mode me hi wapas save karte hain
        # (GitHub Actions me har run naya refresh khud ho jata hai, save karne ki zaroorat nahi)
        if not os.environ.get("BLOGGER_TOKEN_JSON"):
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_data, f)

    return build("blogger", "v3", credentials=creds)


def publish_post(title: str, html_content: str, publish: bool = True) -> dict:
    """
    Blog post publish karta hai.
    publish=True  -> turant live publish ho jayega
    publish=False -> draft ke tor par save hoga (review ke liye)
    """
    service = get_blogger_service()

    body = {
        "kind": "blogger#post",
        "title": title,
        "content": html_content,
    }

    result = service.posts().insert(
        blogId=BLOG_ID,
        body=body,
        isDraft=not publish,
    ).execute()

    return result


if __name__ == "__main__":
    # Quick manual test: python blogger_publish.py
    test_result = publish_post(
        title="Test Post — Ignore",
        html_content="<p>Ye ek test post hai automation check karne ke liye.</p>",
        publish=False,  # draft rakha hai taake accidentally live na ho jaye
    )
    print("Post created! URL:", test_result.get("url"))
    print("Status:", test_result.get("status"))
