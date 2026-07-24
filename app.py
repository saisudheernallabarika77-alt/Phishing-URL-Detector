from flask import Flask, render_template, request
import re
from urllib.parse import urlparse

app = Flask(__name__)

SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd"]
SUSPICIOUS_WORDS = ["login", "verify", "account", "update", "secure", "banking", "confirm", "signin"]


def analyze_url(url):
    score = 0
    reasons = []

    parsed = urlparse(url)
    domain = parsed.netloc

    ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if re.match(ip_pattern, domain):
        score += 3
        reasons.append("URL uses an IP address instead of a domain name")

    if "@" in url:
        score += 3
        reasons.append("URL contains '@' symbol (common phishing trick)")

    if any(shortener in domain for shortener in SHORTENERS):
        score += 2
        reasons.append("URL uses a link shortening service")

    if domain.count(".") > 3:
        score += 2
        reasons.append("URL has an unusually high number of subdomains")

    for word in SUSPICIOUS_WORDS:
        if word in url.lower():
            score += 1
            reasons.append(f"URL contains suspicious keyword: '{word}'")

    if len(url) > 75:
        score += 1
        reasons.append("URL is unusually long")

    if parsed.scheme != "https":
        score += 2
        reasons.append("URL does not use HTTPS")

    if domain.count("-") > 1:
        score += 1
        reasons.append("Domain contains multiple hyphens")

    if score >= 6:
        verdict = "Phishing"
    elif score >= 3:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    return verdict, score, reasons


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            verdict, score, reasons = analyze_url(url)
            result = {
                "url": url,
                "verdict": verdict,
                "score": score,
                "reasons": reasons
            }
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=False)
