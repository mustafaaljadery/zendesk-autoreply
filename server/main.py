import openai
import pinecone
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Initialize CORS with your Flask app

openai.api_key = os.environ.get("OPENAI_API_KEY")

pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment=os.environ.get("PINECONE_ENVIRONMENT")
)

MODEL = "text-embedding-ada-002"


@app.route("/", methods=['GET'])
def index():
    try:
        index = pinecone.Index('openai')
        message = request.args.get('message')
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

        return jsonify({"message": value})
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong"})


if __name__ == '__main__':
    app.run(debug=True)
