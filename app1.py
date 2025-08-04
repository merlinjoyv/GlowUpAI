from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "GlowUpAI Backend is running! Put your HTML file at the same level as this Python file."

@app.route('/submit-user', methods=['POST'])
def submit_user():
    try:
        data = request.json
        
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        timestamp = data.get('timestamp')
        
        csv_file = 'submissions.csv'
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(['Name', 'Email', 'Phone', 'Timestamp'])
            
            writer.writerow([name, email, phone, timestamp])
        
        print(f"✅ Data saved: {name}, {email}, {phone}")
        
        return jsonify({
            'success': True, 
            'message': 'Data saved to CSV successfully!'
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting GlowUpAI Backend...")
    print("📁 Make sure your HTML file is in the same folder as this Python file")
    print("🌐 Backend will run on http://localhost:5000")

    app.run(debug=True, port=5000)
