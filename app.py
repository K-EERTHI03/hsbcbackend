from flask import Flask, send_file, render_template, request, jsonify
from flask_cors import CORS
from main import create_sample_statement
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-statement', methods=['POST'])
def generate_statement():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'cardNumber', 'email', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Generate statement with user data
        create_sample_statement(
            name=data['name'],
            card_number=data['cardNumber'],
            email=data['email'],
            phone=data['phone']
        )
        
        # Check if file exists before sending
        if os.path.exists('credit_card_statement.pdf'):
            return send_file('credit_card_statement.pdf',
                           mimetype='application/pdf',
                           as_attachment=True,
                           download_name='credit_card_statement.pdf')
        else:
            return jsonify({'error': 'Failed to generate PDF'}), 500
            
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({'error': 'Error generating statement. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)