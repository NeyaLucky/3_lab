from flask import Flask

app = Flask(__name__)

@app.route('/api/v1/hello-world-<int:variant_number>')
def hello_world(variant_number):
    response_text = f'Hello World {variant_number}'
    return response_text, 200

if __name__ == '__main__':
    app.run(debug=True)
