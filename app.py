from flask import Flask, render_template, request
from utils.github import search_github_leaks
from dotenv import load_dotenv
load_dotenv()  # Load .env file

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    brand = ""
    if request.method == "POST":
        brand = request.form.get("brand")
        if brand:
            results = search_github_leaks(brand)
    return render_template("index.html", results=results, brand=brand)

if __name__ == "__main__":
    app.run(debug=True)
