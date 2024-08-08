import os
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_health_advice(symptoms):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a helpful and knowledgeable health assistant."
            }, {
                "role": "user",
                "content": f"I have the following symptoms: {symptoms}. Can you provide me with some advice or information on what might be the issue and what steps I should take? and prescribe medicines"
            }]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Health Assistant</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
            color: #343a40;
            font-family: Arial, sans-serif;
        }
        .container {
            margin-top: 50px;
        }
        .health-card {
            background-color: #ffffff;
            border: none;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .health-card__header {
            background-color: #007bff;
            color: #ffffff;
            font-weight: bold;
        }
        .button--primary {
            background-color: #007bff;
            border: none;
            color: #ffffff;
        }
        .button--primary:hover {
            background-color: #0056b3;
        }
        .button--secondary {
            background-color: #6c757d;
            border: none;
            color: #ffffff;
        }
        .button--secondary:hover {
            background-color: #5a6268;
        }
        .health-output {
            background-color: #f8f9fa;
            border: none;
        }
        .navbar {
            background-color: #007bff;
        }
        .navbar__brand, .navbar__link {
            color: #ffffff !important;
        }
        .footer {
            background-color: #007bff;
            color: #ffffff;
            padding: 20px 0;
            position: relative;
            width: 100%;
            bottom: 0;
        }
        .subscribe-form__input {
            border: none;
            padding: 10px;
            width: 70%;
            border-radius: 5px 0 0 5px;
        }
        .subscribe-form__button {
            padding: 10px 20px;
            background-color: #0056b3;
            border: none;
            color: #ffffff;
            border-radius: 0 5px 5px 0;
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelector('#health-form').addEventListener('submit', async (event) => {
                event.preventDefault();
                const symptoms = document.querySelector('#symptoms').value;
                const output = document.querySelector('#output');
                output.textContent = 'Fetching advice...';

                const response = await fetch('/get_advice', {
                    method: 'POST',
                    body: new FormData(event.target)
                });

                const result = await response.json();
                output.textContent = result.advice;
            });
        });

        function copyToClipboard() {
            const output = document.querySelector('#output');
            const textarea = document.createElement('textarea');
            textarea.value = output.textContent;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('Copied to clipboard');
        }
    </script>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar__brand" href="#">Health Assistant</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="navbar__link nav-link" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="navbar__link nav-link" href="#">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="navbar__link nav-link" href="#">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        <h1 class="my-4 text-center">Personal Health Assistant</h1>
        <form id="health-form" class="mb-3">
            <div class="mb-3">
                <label for="symptoms" class="form-label">Describe Your Symptoms:</label>
                <input type="text" class="form-control" id="symptoms" name="symptoms" placeholder="Enter your symptoms here" required>
            </div>
            <div class="text-center">
                <button type="submit" class="button--primary btn">Get Advice</button>
            </div>
        </form>
        <div class="card health-card">
            <div class="card-header health-card__header d-flex justify-content-between align-items-center">
                Output:
                <button class="button--secondary btn btn-sm" onclick="copyToClipboard()">Copy</button>
            </div>
            <div class="card-body">
                <pre id="output" class="health-output mb-0" style="white-space: pre-wrap;"></pre>
            </div>
        </div>

        <div class="my-4">
            <h4>Subscribe to our newsletter</h4>
            <form class="subscribe-form d-flex">
                <input type="email" class="subscribe-form__input form-control me-2" placeholder="Enter your email" required>
                <button type="submit" class="subscribe-form__button btn">Subscribe</button>
            </form>
        </div>
    </div>

    <footer class="footer text-center">
        <div class="container">
            <p>&copy; 2024 Health Assistant. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
    ''')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    symptoms = request.form['symptoms']
    advice = get_health_advice(symptoms)
    return jsonify(advice=advice)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
