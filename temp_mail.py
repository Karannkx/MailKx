import random
import string
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
emails = {}


def generate_email():
    email = ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + '@tempmail.com'
    return email


@app.route('/generate', methods=['GET'])
def generate():
    email = generate_email()
    emails[email] = []
    return jsonify({'email': email})


@app.route('/check', methods=['POST'])
def check():
    email = request.json.get('email')
    if email in emails:
        otp = ''.join(random.choice(string.digits) for _ in range(6))
        emails[email].append(otp)
        return jsonify({'otp': otp})
    else:
        return jsonify({'error': 'Email not found.'}), 404


@app.route('/get_emails', methods=['GET'])
def get_emails():
    return jsonify({'emails': list(emails.keys())})


@app.route('/get_otp', methods=['POST'])
def get_otp():
    email = request.json.get('email')
    if email in emails and len(emails[email]) > 0:
        return jsonify({'otp': emails[email].pop(0)})
    else:
        return jsonify({'error': 'No OTP available.'}), 404


if __name__ == '__main__':
    app.run()
