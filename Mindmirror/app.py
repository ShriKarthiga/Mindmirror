from flask import Flask, render_template, request
import json
from collections import Counter

app = Flask(__name__)

# Load questions once at startup
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Load personality descriptions (match types used in questions)
with open("results.json", "r", encoding="utf-8") as f:
    result_descriptions = json.load(f)

@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        scores = Counter()

        for i in range(len(questions)):
            selected_key = request.form.get(f"q{i}")
            if selected_key:
                option = questions[i]["options"].get(selected_key)
                if option and isinstance(option, dict) and "type" in option:
                    selected_type = option["type"]
                    scores[selected_type] += 1

        if scores:
            result_type = scores.most_common(1)[0][0]
            description = result_descriptions.get(result_type, "Description not found.")
        else:
            result_type = "Unknown"
            description = "No answers were selected."

        return render_template("result.html", personality=result_type.title(), description=description)

    return render_template("quiz.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
