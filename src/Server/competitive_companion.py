from flask import Flask, request, jsonify

app = Flask(__name__)

received_input_data = None
received_output_data = None

@app.route('/', methods=['POST'])
def parse():
    global received_input_data
    global received_output_data
    data = request.get_json()

    if 'tests' in data and data['tests']:
        received_test_case = data['tests'][0] 
        input_data = received_test_case['input']
        received_input_data = input_data
        output_data = received_test_case['output']
        received_output_data = output_data
        return jsonify({"status": "Test case received"}), 200
    else:
        return jsonify({"error": "No test cases found"}), 400

def get_received_test_case():
    global received_input_data
    global received_output_data
    if received_input_data is None or received_output_data is None:
        return None
    return received_input_data, received_output_data
def run_flask_server():
    app.run(host='localhost', port=10045, debug=False)
