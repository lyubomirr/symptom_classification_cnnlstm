from flask import Flask, render_template, request, jsonify
from model import predict

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    symptom, confidence = predict(request.form["text"])
    return jsonify({"class": symptom, "confidence": confidence})

if __name__ == '__main__':
    app.run()