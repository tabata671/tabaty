from flask import Flask, render_template, request
from google import genai
from pydantic import BaseModel
import os
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/gemini" , methods = ["POST"])
def gemini():
    class Events(BaseModel):
        Events: str
        ingredients: list[str]  

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    favorite_event= request.form["favorite_event"]
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{favorite_event}に関連するイベント情報を調べてください",
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Events],
        },
    )
    # Use the response as a JSON string.
    print(response.text)
    return response.text
