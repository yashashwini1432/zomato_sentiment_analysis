import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
from modules.preprocessing import clean_text, detect_language
from modules.sentiment_model import analyze_sentiment

# -------------------------------
# LOGIN CHECK
# -------------------------------
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Login Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.page = "upload"
                st.success("Login successful!")
                st.rerun()  # Changed from experimental_rerun to rerun
            else:
                st.error("Invalid credentials")
        st.stop()

# -------------------------------
# PAGE: UPLOAD + MANUAL REVIEWS
# -------------------------------
def page_upload():
    st.title("📁 Upload or Enter Reviews")

    uploaded_file = st.file_uploader("Upload CSV file (must contain 'review_text')", type=["csv"])
    manual_reviews = st.text_area("Or manually enter reviews (one per line)", height=150)

    combined_df = pd.DataFrame(columns=["review_text"])

    if uploaded_file:
        csv_df = pd.read_csv(uploaded_file)
        if "review_text" not in csv_df.columns:
            st.error("CSV must contain 'review_text' column")
            return
        combined_df = pd.concat([combined_df, csv_df], ignore_index=True)

    if manual_reviews.strip():
        manual_lines = [line.strip() for line in manual_reviews.strip().split("\n") if line.strip()]
        manual_df = pd.DataFrame(manual_lines, columns=["review_text"])
        combined_df = pd.concat([combined_df, manual_df], ignore_index=True)

    if not combined_df.empty:
        combined_df["cleaned_text"] = combined_df["review_text"].apply(clean_text)
        combined_df["language"] = combined_df["review_text"].apply(detect_language)
        st.session_state.df = combined_df
        st.success("Reviews processed successfully!")
        if st.button("Next"):
            st.session_state.page = "analyze"
            st.rerun()  # Changed from experimental_rerun to rerun

# -------------------------------
# PAGE: SENTIMENT ANALYSIS
# -------------------------------
def page_analyze():
    st.title("🧠 Sentiment Analysis")

    df = st.session_state.df
    selected_lang = st.selectbox("Select Language to Analyze", options=df["language"].unique())
    lang_df = df[df["language"] == selected_lang]

    lang_df[["sentiment_score", "sentiment_label"]] = lang_df["cleaned_text"].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )
    st.session_state.df = lang_df

    st.success("Sentiment analysis complete!")
    if st.button("Next"):
        st.session_state.page = "visualize"
        st.rerun()  # Changed from experimental_rerun to rerun

# -------------------------------
# PAGE: VISUALIZATIONS
# -------------------------------
def page_visualize():
    st.title("📊 Visualizations")

    df = st.session_state.df

    st.subheader("📈 Sentiment Distribution")
    sentiment_counts = df["sentiment_label"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    chart = alt.Chart(sentiment_counts).mark_bar().encode(
        x="Sentiment",
        y="Count",
        color=alt.Color("Sentiment", scale=alt.Scale(
            domain=["Positive", "Neutral", "Negative"],
            range=["#4CAF50", "#FFC107", "#F44336"]
        ))
    ).properties(width=600)

    st.altair_chart(chart)

    st.subheader("☁ Word Cloud")
    all_text = " ".join(df["cleaned_text"])
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
    plt.figure(figsize=(10, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt.gcf())  # FIXED ✅

    if st.button("Next"):
        st.session_state.page = "sample"
        st.rerun()  # Changed from experimental_rerun to rerun

# -------------------------------
# PAGE: SAMPLE REVIEWS
# -------------------------------
def page_sample():
    st.title("💬 Sample Reviews")
    df = st.session_state.df
    st.dataframe(df[["review_text", "sentiment_score", "sentiment_label"]])
    if st.button("Next"):
        st.session_state.page = "export"
        st.rerun()  # Changed from experimental_rerun to rerun

# -------------------------------
# PAGE: EXPORT + LOGOUT
# -------------------------------
def page_export():
    st.title("📤 Export Report & Logout")
    df = st.session_state.df

    if st.button("Export PDF Report"):
        sentiment_counts = df["sentiment_label"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Zomato Sentiment Analysis Report", ln=True, align="C")
        for index, row in sentiment_counts.iterrows():
            pdf.cell(200, 10, txt=f"{row['Sentiment']}: {row['Count']}", ln=True)

        pdf_bytes = pdf.output(dest="S").encode("latin1")
        buffer = BytesIO(pdf_bytes)

        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="sentiment_report.pdf",
            mime="application/pdf"
        )

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()  # Changed from experimental_rerun to rerun

# -------------------------------
# MAIN FLOW
# -------------------------------
def main():
    check_login()
    if "page" not in st.session_state:
        st.session_state.page = "upload"

    page = st.session_state.page
    page_dict = {
        "upload": page_upload,
        "analyze": page_analyze,
        "visualize": page_visualize,
        "sample": page_sample,
        "export": page_export,
    }

    current_page = page_dict.get(page, page_upload)
    current_page()

if __name__ == "__main__":
    main()


