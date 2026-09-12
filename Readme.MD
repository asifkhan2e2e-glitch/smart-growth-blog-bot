# Smart Growth Blog Bot

Automated blog content generator aur publisher — Groq AI se content generate karta hai aur khud-ba-khud Blogger par publish karta hai, GitHub Actions ke zariye har hafte.

**Blog:** Smart Growth: AI — [smartcareerai.blogspot.com](https://smartcareerai.blogspot.com/)

---

## Ye system kya karta hai

1. `topics.json` se agla pending topic uthata hai (AI & Technology, Education & Career, Personal Finance — rotation me)
2. Groq API (model: `openai/gpt-oss-120b`) se poora blog post generate karta hai
3. Blogger API v3 ke zariye directly live publish kar deta hai
4. `topics.json` aur `publish_log.json` update kar deta hai taake track rahe kya publish ho chuka hai
5. **GitHub Actions** har Tuesday, subah 10:00 AM (Pakistan time) par ye poora process khud chalata hai — koi manual kaam nahi

---

## Files ka kaam

| File | Kaam |
|------|------|
| `main.py` | Asal script — sab kuch isi ko chalana hai |
| `content_generator.py` | Groq API se content generate karta hai |
| `blogger_publish.py` | Blogger par publish karta hai |
| `blogger_auth.py` | Ek-baar wali authorization (setup ke waqt) |
| `list_my_blogs.py` | Blog ID nikalne ke liye (setup ke waqt) |
| `topics.json` | 18-hafton ki topics list, status ke sath |
| `publish_log.json` | Kaunse blogs kab publish hue, uska record |
| `.github/workflows/publish-blog.yml` | GitHub Actions ka schedule |

---

## Local setup (pehli baar, apne computer par)

1. Python install karein (agar nahi hai)
2. Is repo ko clone/download karein
3. `client_secret_blogger.json` (Google Cloud se) is folder me daalein
4. Terminal me:
   ```
   pip install -r requirements.txt
   ```
5. Blogger authorize karein (sirf ek baar):
   ```
   python blogger_auth.py
   ```
   Ye `token_blogger.json` bana dega.
6. Blog ID confirm karein:
   ```
   python list_my_blogs.py
   ```
7. `.env.example` ko rename kar ke `.env` banayein, usme apni Groq API key daalein:
   ```
   GROQ_API_KEY=aapki_asal_key
   ```
8. Test run karein:
   ```
   python main.py
   ```

---

## GitHub Actions setup (automation ke liye)

Repository ke **Settings → Secrets and variables → Actions** me ye 2 secrets add karein:

| Secret Name | Value |
|-------------|-------|
| `GROQ_API_KEY` | Aapki Groq API key |
| `BLOGGER_TOKEN_JSON` | Aapki `token_blogger.json` file ka poora content |

Iske baad workflow khud Tuesday subah chalega. Manual test ke liye: **Actions tab → Weekly Blog Publish → Run workflow**

---

## ⚠️ Zaroori — kabhi share/upload na karein

- `client_secret_blogger.json`
- `token_blogger.json`
- `.env` (asal Groq key wali)

Ye sab `.gitignore` me already exclude hain, lekin dhyan rakhna zaroori hai.

---

## Medium ke baare me

Medium ka official API 2023 se deprecated hai aur naye accounts ke liye integration token nahi milta — is liye Medium par publishing filhal **manual** hai. Content generate ho kar ready rakha ja sakta hai, phir copy-paste kar ke Medium par publish karna hota hai.

---

## Content niche

**Smart Growth: AI, Career & Money** — teen categories rotate hoti hain:
- 🤖 AI & Technology
- 🎓 Education & Career
- 💰 Personal Finance
