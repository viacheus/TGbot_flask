from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    prompt = data.get("prompt", "")
    response = f"Received: {prompt}"
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)