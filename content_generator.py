"""
Ye module Groq API use karke ek topic se poora blog post generate karta hai.
Isay directly nahi chalana — ye 'main.py' ke andar use hota hai.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Model choice: gpt-oss-120b Groq ke free/developer tier me available hai
# (llama-3.3-70b-versatile ab sirf Enterprise tier ke liye reh gaya hai)
MODEL_NAME = "openai/gpt-oss-120b"


def generate_blog_post(topic: str) -> dict:
    """
    Topic le kar Groq se ek poora blog post generate karta hai.
    Return karta hai: {"title": ..., "html_content": ...}
    """

    system_prompt = (
        "You are an expert blog writer for a website about AI, career growth, "
        "and personal finance. Write in a clear, engaging, practical tone with "
        "real examples. Avoid generic filler sentences. Structure the post with "
        "an introduction, 3-5 subheadings using <h3> tags, bullet points where "
        "useful using <ul><li>, and a short conclusion. "
        "Output ONLY valid HTML for the blog body (no <html> or <body> tags, "
        "just the content itself: <p>, <h3>, <ul>, <li>, <strong> tags allowed). "
        "Do not include a title inside the HTML body."
    )

    user_prompt = (
        f"Write a complete, well-structured blog post (700-1000 words) on this topic: "
        f"'{topic}'. Make it genuinely useful and specific, not generic."
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=2000,
    )

    html_content = response.choices[0].message.content.strip()

    return {
        "title": topic,
        "html_content": html_content,
    }


if __name__ == "__main__":
    # Quick manual test: python content_generator.py
    test_topic = "5 AI Tools Every Student Should Know in 2026"
    result = generate_blog_post(test_topic)
    print("TITLE:", result["title"])
    print("\n--- CONTENT PREVIEW ---\n")
    print(result["html_content"][:500])
