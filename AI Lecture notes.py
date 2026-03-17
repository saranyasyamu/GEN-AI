import streamlit as st
import fitz
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import random

nltk.download('punkt')

st.set_page_config(page_title="AI Lecture Notes Summarizer", layout="wide")

# ---------------------------
# ULTIMATE WHITE UI STYLE
# ---------------------------
st.markdown("""
<style>

.stApp{
background-color:white;
color:black;
}

h1,h2,h3{
color:black;
}

.card{
background:#f8f9fa;
padding:20px;
border-radius:10px;
margin-bottom:20px;
box-shadow:0px 2px 6px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

st.title("📚 AI Lecture Notes Summarizer")
st.write("Upload lecture notes PDF to generate summary, key points, flashcards and MCQ quiz.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# ---------------------------
# PDF TEXT EXTRACTION
# ---------------------------
def extract_text(pdf):
    text = ""
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    
    for page in doc:
        text += page.get_text()
        
    return text


# ---------------------------
# SUMMARY USING TOKENIZATION
# ---------------------------
def summarize_text(text, n=5):

    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    word_freq = Counter(words)

    sentence_scores = {}

    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]

    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]

    return summary_sentences


# ---------------------------
# KEY POINT EXTRACTION
# ---------------------------
def key_points(text, n=5):

    sentences = sent_tokenize(text)

    return sentences[:n]


# ---------------------------
# FLASHCARD GENERATION
# ---------------------------
def generate_flashcards(text):

    sentences = sent_tokenize(text)

    flashcards = []

    for i in range(min(5, len(sentences))):

        question = "What does the following statement explain?"
        answer = sentences[i]

        flashcards.append((question, answer))

    return flashcards


# ---------------------------
# MCQ GENERATION
# ---------------------------
def generate_mcq(text):

    sentences = sent_tokenize(text)
    words = list(set(word_tokenize(text)))

    mcqs = []

    for i in range(3):

        sentence = sentences[i]

        correct = random.choice(word_tokenize(sentence))

        options = [correct]

        while len(options) < 4:
            option = random.choice(words)
            if option not in options and option.isalpha():
                options.append(option)

        random.shuffle(options)

        question = sentence.replace(correct, "___")

        mcqs.append((question, options, correct))

    return mcqs


# ---------------------------
# MAIN APP
# ---------------------------
if uploaded_file:

    text = extract_text(uploaded_file)

    summary = summarize_text(text)
    points = key_points(text)
    cards = generate_flashcards(text)
    mcqs = generate_mcq(text)

    # ---------------------------
    # SLIDES MENU (SIDEBAR)
    # ---------------------------
    page = st.sidebar.radio(
        "Slides Menu",
        ["📄 Extracted Text", "🧠 Summary", "⭐ Key Points", "🧾 Flashcards", "📝 Quiz"]
    )

    # ---------------------------
    # SLIDE 1
    # ---------------------------
    if page == "📄 Extracted Text":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("Extracted Text")

        st.text_area("", text[:2000], height=400)

        st.markdown("</div>", unsafe_allow_html=True)


    # ---------------------------
    # SLIDE 2
    # ---------------------------
    elif page == "🧠 Summary":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("Summary")

        for s in summary:
            st.write("•", s)

        st.markdown("</div>", unsafe_allow_html=True)


    # ---------------------------
    # SLIDE 3
    # ---------------------------
    elif page == "⭐ Key Points":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("Key Points")

        for p in points:
            st.write("•", p)

        st.markdown("</div>", unsafe_allow_html=True)


    # ---------------------------
    # SLIDE 4
    # ---------------------------
    elif page == "🧾 Flashcards":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("Flashcards")

        for i, (q, a) in enumerate(cards):

            with st.expander(f"Flashcard {i+1}"):

                st.write("Question:")
                st.write(q)

                st.write("Answer:")
                st.write(a)

        st.markdown("</div>", unsafe_allow_html=True)


    # ---------------------------
    # SLIDE 5
    # ---------------------------
    elif page == "📝 Quiz":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("MCQ Quiz")

        score = 0

        for i, (q, options, correct) in enumerate(mcqs):

            st.write(f"Q{i+1}. {q}")

            user_ans = st.radio("Choose answer", options, key=i)

            if user_ans == correct:
                score += 1

        if st.button("Submit Quiz"):

            percent = (score / len(mcqs)) * 100

            st.success(f"Score: {score} / {len(mcqs)}")
            st.progress(percent / 100)

            st.write(f"Percentage: {percent:.2f}%")

        st.markdown("</div>", unsafe_allow_html=True)