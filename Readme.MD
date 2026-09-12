# Smart Growth Blog Bot

An automated blog content generator and publisher — generates content using Groq AI and automatically publishes it to Blogger every week via GitHub Actions.

**Blog:** Smart Growth: AI — [smartcareerai.blogspot.com](https://smartcareerai.blogspot.com/)

---

## What this system does

1. Picks the next pending topic from `topics.json` (rotates through AI & Technology, Education & Career, and Personal Finance)
2. Generates a complete blog post using the Groq API (model: `openai/gpt-oss-120b`)
3. Publishes it live directly via the Blogger API v3
4. Updates `topics.json` and `publish_log.json` to keep track of what has been published
5. **GitHub Actions** runs this whole process automatically every Tuesday at 10:00 AM (Pakistan time) — no manual work needed

---

## What each file does

| File | Purpose |
|------|---------|
| `main.py` | The main script — this is the one you run |
| `content_generator.py` | Generates content using the Groq API |
| `blogger_publish.py` | Publishes the post to Blogger |
| `blogger_auth.py` | One-time authorization script (used only during setup) |
| `list_my_blogs.py` | Fetches your Blog ID (used only during setup) |
| `topics.json` | The 18-week topic list, along with publish status |
| `publish_log.json` | A record of what was published and when |
| `.github/workflows/publish-blog.yml` | The GitHub Actions schedule |

---

## Local setup (first-time, on your own computer)

1. Install Python (if not already installed)
2. Clone/download this repository
3. Place your `client_secret_blogger.json` (from Google Cloud) in this folder
4. In the terminal, run:
   ```
   pip install -r requirements.txt
   ```
5. Authorize Blogger access (only needs to be done once):
   ```
   python blogger_auth.py
   ```
   This will create `token_blogger.json`.
6. Confirm your Blog ID:
   ```
   python list_my_blogs.py
   ```
7. Rename `.env.example` to `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_key_here
   ```
8. Run a test:
   ```
   python main.py
   ```

---

## GitHub Actions setup (for automation)

In the repository, go to **Settings → Secrets and variables → Actions** and add these 2 secrets:

| Secret Name | Value |
|-------------|-------|
| `GROQ_API_KEY` | Your Groq API key |
| `BLOGGER_TOKEN_JSON` | The full contents of your `token_blogger.json` file |

Once added, the workflow will automatically run every Tuesday morning. To test it manually: go to the **Actions tab → Weekly Blog Publish → Run workflow**.

---

## ⚠️ Important — never share or upload these

- `client_secret_blogger.json`
- `token_blogger.json`
- `.env` (the one with your real Groq key)

These are already excluded via `.gitignore`, but it's still important to be careful.

---

## About Medium

Medium's official API has been deprecated since 2023, and new accounts can no longer generate integration tokens — so publishing to Medium is currently a **manual** step. Content can still be generated and kept ready, then copy-pasted to publish on Medium.

---

## Content niche

**Smart Growth: AI, Career & Money** — content rotates across three categories:
- 🤖 AI & Technology
- 🎓 Education & Career
- 💰 Personal Finance
