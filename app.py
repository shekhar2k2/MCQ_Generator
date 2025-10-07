from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

# Load environment variable
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

generation_config = {
    "temperature": 0.1,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json"
}

model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    generation_config = generation_config
)

# MCQ Generator
def generate_mcqs(subject, year_exp, number_of_mcq):

    prompt = f"""
    Generate {number_of_mcq} multiple-choice questions on the topic "{subject}" for someone with {year_exp} year(s) of experience.
    Each question should have:
    - A unique question label (e.g., Q1, Q2, ...)
    - Four answer options (a, b, c, d)
    - Only one correct answer
    Return the response strictly as a valid JSON list in this format:

    [
    {{
        "Q1": "What is the capital of India?",
        "options": {{
        "a": "Delhi",
        "b": "Lucknow",
        "c": "Bihar",
        "d": "Pune"
        }},
        "answer": "a"
    }},
    ...
    ]
    """

    response = model.generate_content(prompt)
    return json.loads(response.text)

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    mcq_output = "response"
    subject = ""
    experience = ""
    number = ""

    if request.method == "POST":
        action = request.form.get("action")
        subject = request.form["subject"]
        experience = request.form["experience"]
        number = request.form["number"]

        if action == "generate":
            mcq_output = generate_mcqs(subject, experience, number)
        elif action == "delete":
            mcq_output = ""  # Only delete the generated result, keep inputs

    return render_template("index.html", result=mcq_output, subject=subject, experience=experience, number=number)


if __name__ == "__main__":
    app.run(debug=True)
