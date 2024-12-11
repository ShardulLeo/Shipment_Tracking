from flask import Flask, render_template, request, jsonify
from utils.db_utils import get_db_connection
from models.predict_cancellation import predict_cancellation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/shipments', methods=['GET'])
def get_shipments():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM shipments")
    shipments = cursor.fetchall()
    db.close()
    return jsonify(shipments)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = predict_cancellation(data)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)