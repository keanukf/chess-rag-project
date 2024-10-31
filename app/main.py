from flask import Flask, request, jsonify
from app.pandasai_query import query_chess_data

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Invalid request, missing "query"'}), 400

        query = data['query']
        response = query_chess_data(query)
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 