import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY','your-key-if-not-using-env')
openai = OpenAI()
sample_reviews = [
        "Great battery life, but the screen could be brighter. Overall satisfied with purchase.",
        "The camera quality exceeded my expectations. Night mode is fantastic!",
        "Setup was a bit complicated. Customer service wasn't very helpful.",
        "Perfect size and weight. Would definitely recommend to others."
    ]
combined_reviews = "\n".join([f"- {review}" for review in sample_reviews])
product_name = "Smartphone X"
# Create prompt for the API
product_context = f"for the product Smartphone X"
prompt = f"""Please analyze these product reviews {product_context}and provide:
        1. A concise summary of the main points
        2. Key pros and cons
        3. Overall sentiment
        4. Most commonly mentioned features
        
Reviews:
    {combined_reviews}"""
response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful product review analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
summary = response.choices[0].message.content

print(summary)