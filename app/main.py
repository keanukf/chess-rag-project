from flask import Flask, request, jsonify
from app.langchain_sql_agent import execute_query

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Invalid request, missing "query"'}), 400

        query = data['query']
        response = execute_query(query)
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)