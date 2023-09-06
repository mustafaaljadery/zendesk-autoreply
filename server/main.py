import openai
import pinecone
from flask import Flask, redirect, render_template, request, url_for
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)

MODEL = "text-embedding-ada-002"


@app.route("/")
def index():
    index = pinecone.Index('openai')
    message = request.json.get("message")
    xq = openai.Embedding.create(input=message, engine=MODEL)[
        'data'][0]['embedding']
    res = index.query([xq], top_k=5, include_metadata=True)
    text_input = [record['metadata']['text'] for record in res["matches"]]
    text_input = '\n'.join(text_input)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are the most helpful customer support expert in the whole world! Answer the users question with the context provided."},
            {"role": "user", "content": f"""Question: {message}
            Context: {text_input}
            Answer:
             """},
        ]
    )

    value = response.choices[0].message.content
    return value
