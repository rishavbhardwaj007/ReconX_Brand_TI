from flask import Flask, render_template, request
from utils.github import search_github_leaks
from utils.telegram_utils import send_telegram_alert
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    brand = ""
    if request.method == "POST":
        brand = request.form.get("brand")
        if brand:
            results = search_github_leaks(brand)

            # Send alert
            if results:
                for item in results:
                    msg = f"🚨 *Leak Found for {brand}*\n*Repo:* {item['repo']}\n*File:* {item['path']}\n[View Leak]({item['url']})"
                    send_telegram_alert(msg)

    return render_template("index.html", results=results, brand=brand)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
