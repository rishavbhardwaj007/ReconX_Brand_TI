from flask import Flask, render_template, request
from dotenv import load_dotenv
from utils.github import search_github_leaks
from utils.telegram_utils import send_telegram_alert, search_telegram
from utils.darkweb import search_darkweb
from utils.enrich import shodan_search

load_dotenv()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    github_results = []
    telegram_results = ""
    darkweb_results = ""
    shodan_results = ""
    brand = ""

    if request.method == "POST":
        brand = request.form.get("brand")
        if brand:
            github_results = search_github_leaks(brand)
            telegram_results = search_telegram(brand)
            darkweb_results = search_darkweb(brand)
            shodan_results = shodan_search(brand)

            if github_results:
                for item in github_results:
                    msg = f"\ud83d\udea8 *Leak Found for {brand}*\n*Repo:* {item['repo']}\n*File:* {item['path']}\n[View Leak]({item['url']})"
                    send_telegram_alert(msg)

    return render_template(
        "index.html",
        github_results=github_results,
        telegram_results=telegram_results,
        darkweb_results=darkweb_results,
        shodan_results=shodan_results,
        brand=brand
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
