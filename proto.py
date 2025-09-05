from flask import Flask, render_template, request, jsonify
import pandas as pd
from rapidfuzz import fuzz

app = Flask(__name__)

data = pd.read_csv("basic.csv", quotechar='"')

def get_response(user_input):
    user_input_lower = user_input.lower()
    best_score = 0
    best_row = None

    for _, row in data.iterrows():
        keywords = [kw.strip() for kw in row['Keywords'].split(',')]
        keyword_score = max([fuzz.partial_ratio(user_input_lower, kw.lower()) for kw in keywords])
        sentence_score = fuzz.token_sort_ratio(user_input_lower, str(row['Response']).lower())
        weighted_score = (0.6 * keyword_score + 0.4 * sentence_score) * float(row['ScoreWeight'])

        if weighted_score > best_score:
            best_score = weighted_score
            best_row = row
    
    if best_row is not None and best_score >= 60:
        return best_row['Response']
    else:
        return "I’m not sure how to respond."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
