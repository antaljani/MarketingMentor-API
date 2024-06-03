from flask import Flask, request, jsonify
from openai import OpenAI
import prompts as p
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
# API hívás a "Marketing Mentor" egyéni GPT modellhez

client = OpenAI(api_key=os.getenv("API_KEY"))

def buyer_persona(input_data):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": p.buyer_persona},
            {"role": "user", "content": f"Készíts nekem egy vevői avatárt a következő információk alapján: {input_data}"}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route('/buyer_persona', methods=['GET'])
def create_buyer_persona():
    input_data = request.args.get('input')  # Szöveg beolvasása a GET paraméterből
    if not input_data:
        return jsonify({"error": "Input data is required"}), 400
    
    try:
        result = buyer_persona(input_data)
        return jsonify({"buyer_persona": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
