import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import numpy as np
from typing import List


# Page configuration
st.set_page_config(page_title="Review Summarizer", page_icon="📝")

# Load environment variables in a file called .env
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Check the key
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

openai = OpenAI()

def summarize_reviews(reviews, max_tokens=150):
    try:
        # Combine reviews into a single string
        combined_reviews = "\n".join(reviews)
        
        # Create the prompt
        prompt = f"""Please analyze these customer reviews and provide a concise summary that includes:
        1. What do customers say?
        2. Main sentiment (positive/negative/mixed)
        3. Key recurring themes
        4. Most common praise points
        5. Most common complaints
        6. Suggested areas for improvement

        Reviews:
        {combined_reviews}"""

        # Make API call to OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes customer reviews."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.5
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during summarization: {str(e)}"

def main():
    st.title("📝 Review Summarizer")
    st.write("Upload your reviews as a CSV file or paste them directly to get an AI-powered summary.")

    
    # Input method selection
    input_method = st.radio("Choose input method:", ["Upload CSV", "Paste Text"])

    reviews = []
    
    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                # Allow user to select the review column
                review_column = st.selectbox("Select the column containing reviews:", df.columns)
                reviews = df[review_column].tolist()
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")

    else:  # Paste Text
        text_input = st.text_area("Paste your reviews here (one review per line):", height=200)
        if text_input:
            reviews = text_input.split('\n')
            # Remove empty lines
            reviews = [r for r in reviews if r.strip()]

    if reviews:
        st.write(f"Number of reviews loaded: {len(reviews)}")
        
        # Sample of reviews
        with st.expander("View sample of reviews"):
            st.write(reviews[:5])

        # Summarization parameters
        max_tokens = st.slider("Maximum length of summary (in tokens):", 100, 500, 150)
        
        if st.button("Summarize Reviews"):
            with st.spinner("Analyzing reviews..."):
                summary = summarize_reviews(reviews, max_tokens)
                st.markdown("### Summary")
                st.write(summary)

                # Option to download summary
                summary_text = f"Review Summary\n\nNumber of reviews analyzed: {len(reviews)}\n\n{summary}"
                st.download_button(
                    label="Download Summary",
                    data=summary_text,
                    file_name="review_summary.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()