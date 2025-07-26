from flask import Flask, request, jsonify
from complaint_analyzer import analyze_complaint
import os

app = Flask(__name__)

REASON_JSON_PATH = os.path.join(os.path.dirname(__file__), 'reason_type_mapping.json')

@app.route('/analyze-complaint', methods=['POST'])
def analyze_complaint_api():
    data = request.get_json()
    sentence = data.get('sentence', '')
    result = analyze_complaint(sentence, REASON_JSON_PATH)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

