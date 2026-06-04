from flask import Flask, render_template, request, jsonify
from summarizer import summarize_text

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():

    try:

        data = request.get_json()

        text = data.get("text", "")

        if len(text.strip()) < 50:
            return jsonify({
                "error": "Please enter at least 50 characters."
            })

        result = summarize_text(text)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)