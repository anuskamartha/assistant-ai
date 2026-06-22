import os
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from PIL import Image
import pytesseract

# =========================
# API KEY
# =========================

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Assistant")

# =========================
# FILE UPLOADS
# =========================

uploaded_pdf = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

question = st.text_area(
    "Ask your question"
)

context = ""

# =========================
# PDF PROCESSING
# =========================

if uploaded_pdf is not None:
    reader = PdfReader(uploaded_pdf)

    for page in reader.pages:
        text = page.extract_text()

        if text:
            context += text + "\n"

# =========================
# IMAGE PROCESSING
# =========================

if uploaded_image is not None:
    image = Image.open(uploaded_image)

    st.image(image, caption="Uploaded image", use_container_width=True)

    image_text = pytesseract.image_to_string(image)

    context += "\n" + image_text

# =========================
# AI RESPONSE
# =========================

if st.button("Submit"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    prompt = f"""
You are an AI study assistant.

Use the provided content to answer the question accurately and clearly.

CONTENT:
{context[:12000]}

QUESTION:
{question}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1024
        )

        answer = response.choices[0].message.content

        st.subheader("Answer")
        st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")
