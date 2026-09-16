"""
Smart Growth Blog Bot — Dashboard
Ye Streamlit app topics.json aur publish_log.json padh kar status dikhata hai,
aur ek chat assistant deta hai jisse blog-related sawal poochhe ja sakein.

Chalane ka tareeqa (isi blog_automation folder ke andar):
    streamlit run app.py
"""

import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(page_title="Smart Growth Blog Bot", page_icon="📝", layout="wide")

TOPICS_FILE = "topics.json"
LOG_FILE = "publish_log.json"


# ---------- Data loading ----------

def load_topics():
    if not os.path.exists(TOPICS_FILE):
        return []
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


topics = load_topics()
log = load_log()

published = [t for t in topics if t.get("status") == "published"]
pending = [t for t in topics if t.get("status") == "pending"]
next_topic = pending[0] if pending else None


# ---------- Header ----------

st.title("📝 Smart Growth Blog Bot")
st.caption("AI, Career & Money — automated blog dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Topics", len(topics))
col2.metric("Published", len(published))
col3.metric("Pending", len(pending))

st.divider()

# ---------- Next topic ----------

st.subheader("📅 Next Scheduled Blog")
if next_topic:
    st.info(
        f"**{next_topic['topic']}**  \n"
        f"Category: {next_topic['category']}  \n"
        f"Runs automatically every Tuesday, 10:00 AM (Pakistan time)"
    )
else:
    st.success("All 18 topics have been published! Time to add a new batch of topics.")

st.divider()

# ---------- Topics table ----------

st.subheader("📋 Full Topic Schedule")

tab1, tab2 = st.tabs(["All Topics", "Publish History"])

with tab1:
    for t in topics:
        status_icon = "✅" if t.get("status") == "published" else "⏳"
        st.write(f"{status_icon} **Week {t['week']}** — [{t['category']}] {t['topic']}")

with tab2:
    if log:
        for entry in reversed(log):
            st.write(f"🟢 **{entry['topic']}**")
            st.write(f"   Published: {entry.get('published_at', 'N/A')}")
            if entry.get("url"):
                st.write(f"   [View post]({entry['url']})")
            st.write("---")
    else:
        st.write("No posts published yet.")

st.divider()

# ---------- Chat Assistant ----------

st.subheader("💬 Ask the Assistant")
st.caption("Ask things like: 'Agla blog kab hai?', 'Kitne blogs publish ho chuke?', 'Kaunsa topic pending hai?'")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_groq_api_key():
    # Streamlit Cloud par: Settings > Secrets se milega
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    # Local computer par: .env file se milega
    return os.environ.get("GROQ_API_KEY")


client = Groq(api_key=get_groq_api_key())


def build_context():
    return (
        f"Total topics: {len(topics)}\n"
        f"Published: {len(published)}\n"
        f"Pending: {len(pending)}\n"
        f"Next topic: {next_topic['topic'] if next_topic else 'None - all done'}\n"
        f"Full topics list: {json.dumps(topics, ensure_ascii=False)}\n"
        f"Publish log: {json.dumps(log, ensure_ascii=False)}\n"
        f"Schedule: Every Tuesday, 10:00 AM Pakistan time, via GitHub Actions.\n"
        f"Blog platform: Blogger (smartcareerai.blogspot.com). "
        f"Medium publishing is currently manual (Medium's API is deprecated for new accounts)."
    )


for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_question = st.chat_input("Apna sawal likhein...")

if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.write(user_question)

    system_prompt = (
        "You are a helpful assistant for a blog automation dashboard. "
        "Answer questions about the blog schedule, topics, and publishing status "
        "using ONLY the data provided below. Reply in the same language style "
        "the user used (Roman Urdu/Hindi or English). Be concise and direct.\n\n"
        f"DATA:\n{build_context()}"
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.chat_history,
        ],
        temperature=0.3,
        max_tokens=500,
    )

    answer = response.choices[0].message.content.strip()
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)
