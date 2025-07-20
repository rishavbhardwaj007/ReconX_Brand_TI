from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from utils.github import search_github_leaks
from utils.telegram_utils import send_telegram_alert, search_telegram
from utils.darkweb import search_darkweb
from utils.enrich import shodan_search
from utils.pastebin import search_pastebin
from utils.reddit import search_reddit
from utils.twitter import search_twitter
from utils.breach_check import check_haveibeenpwned
from utils.dns_enum import dns_enumeration
from utils.openai_analysis import analyze_with_openai, generate_threat_report

load_dotenv()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    github_results = []
    telegram_results = ""
    darkweb_results = ""
    shodan_results = ""
    pastebin_results = []
    reddit_results = []
    twitter_results = []
    breach_results = ""
    dns_results = []
    ai_analysis = ""
    threat_report = ""
    brand = ""

    if request.method == "POST":
        brand = request.form.get("brand")
        if brand:
            # Existing searches
            github_results = search_github_leaks(brand)
            telegram_results = search_telegram(brand)
            darkweb_results = search_darkweb(brand)
            shodan_results = shodan_search(brand)
            
            # New data sources
            pastebin_results = search_pastebin(brand)
            reddit_results = search_reddit(brand)
            twitter_results = search_twitter(brand)
            breach_results = check_haveibeenpwned(brand)
            dns_results = dns_enumeration(brand)
            
            # OpenAI Analysis
            all_results = {
                'github': github_results,
                'telegram': telegram_results,
                'darkweb': darkweb_results,
                'shodan': shodan_results,
                'pastebin': pastebin_results,
                'reddit': reddit_results,
                'twitter': twitter_results,
                'breach': breach_results,
                'dns': dns_results
            }
            
            ai_analysis = analyze_with_openai(brand, all_results)
            threat_report = generate_threat_report(brand, all_results)

            # Send alerts for critical findings
            if github_results:
                for item in github_results:
                    msg = f"🚨 *Leak Found for {brand}*\n*Repo:* {item['repo']}\n*File:* {item['path']}\n[View Leak]({item['url']})"
                    send_telegram_alert(msg)

    return render_template(
        "index.html",
        github_results=github_results,
        telegram_results=telegram_results,
        darkweb_results=darkweb_results,
        shodan_results=shodan_results,
        pastebin_results=pastebin_results,
        reddit_results=reddit_results,
        twitter_results=twitter_results,
        breach_results=breach_results,
        dns_results=dns_results,
        ai_analysis=ai_analysis,
        threat_report=threat_report,
        brand=brand
    )

@app.route("/api/scan", methods=["POST"])
def api_scan():
    """API endpoint for programmatic access"""
    data = request.get_json()
    brand = data.get("brand")
    
    if not brand:
        return jsonify({"error": "Brand name is required"}), 400
    
    results = {
        "brand": brand,
        "github": search_github_leaks(brand),
        "telegram": search_telegram(brand),
        "darkweb": search_darkweb(brand),
        "shodan": shodan_search(brand),
        "pastebin": search_pastebin(brand),
        "reddit": search_reddit(brand),
        "twitter": search_twitter(brand),
        "breach": check_haveibeenpwned(brand),
        "dns": dns_enumeration(brand),
    }
    
    results["ai_analysis"] = analyze_with_openai(brand, results)
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)