from flask import Flask, render_template, request
from google import genai
from pydantic import BaseModel
import os
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

app = Flask(__name__)

google_search_tool = Tool(
    google_search = GoogleSearch()
)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/gemini" , methods = ["POST"])
def gemini():
    class Event(BaseModel):
        event_name: str
    

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    event_place= request.form["event_place"]
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{event_place}で今月行われるイベントの日付と内容を調べてください",
        config=GenerateContentConfig(
            tools=[google_search_tool],
            # response_mime_type= "application/json",
            # response_schema= list[Event],
            response_modalities= ["TEXT"],
        )
         
    )
    # Use the response as a JSON string.
    print(response.text)
    return response.text

