# Project Documentation: Phishing URL Detector

## 1. Problem Statement

Phishing remains one of the most common attack vectors used to steal credentials and sensitive information. Attackers craft URLs that mimic legitimate websites through techniques like IP-based addresses, misleading subdomains, URL shorteners, and lookalike domains. This project provides an automated, rule-based tool to flag such URLs before a user interacts with them.

## 2. Objective

To build a lightweight web application that accepts a URL as input and returns a risk assessment (Safe, Suspicious, or Phishing) based on a transparent, explainable scoring system — rather than a black-box machine learning model — so every verdict can be understood and justified.

## 3. Architecture
**Request flow:**
1. User submits a URL via a POST request on the home route (`/`)
2. `analyze_url()` parses the URL and runs it through 8 independent checks
3. Each triggered check adds to a cumulative risk score and appends a human-readable reason
4. The final score maps to a verdict threshold (Safe / Suspicious / Phishing)
5. Flask renders the result back into `index.html` using Jinja2 templating

## 4. Detection Logic

| # | Check | Weight | Rationale |
|---|-------|--------|-----------|
| 1 | IP address instead of domain | +3 | Legitimate sites almost never use raw IPs |
| 2 | '@' symbol in URL | +3 | Used to disguise the real destination in browsers |
| 3 | Known URL shortener | +2 | Commonly used to hide the actual phishing domain |
| 4 | Excessive subdomains (>3 dots) | +2 | A frequent obfuscation technique |
| 5 | Suspicious keywords (login, verify, secure, etc.) | +1 each | Common in credential-harvesting pages |
| 6 | URL length > 75 characters | +1 | Long URLs often hide malicious parameters |
| 7 | No HTTPS | +2 | Legitimate login pages almost always use HTTPS |
| 8 | Multiple hyphens in domain | +1 | Common in spoofed brand domains (e.g., paypal-secure-login.com) |

Score thresholds:
- **0–2:** Safe
- **3–5:** Suspicious
- **6+:** Phishing

## 5. Design Decisions

- **Rule-based over ML:** Chosen for transparency — every verdict comes with explicit reasons, which matters for a security tool where false positives/negatives need to be explainable.
- **Single-file backend:** Kept `app.py` self-contained for simplicity given the project scope; logic could be split into modules if extended.
- **Dark theme UI:** Matches common security-tool aesthetics and keeps focus on the input/result rather than decoration.

## 6. Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML, CSS (no JS framework — server-rendered via Jinja2)
- **Environment:** Kali Linux, Python virtual environment (venv)

## 7. Possible Extensions

- WHOIS-based domain age lookup
- SSL certificate validation
- Integration with a real-time threat intelligence feed (e.g., PhishTank API)
- Browser extension wrapper for real-time link checking

## 8. How to Run

```bash
git clone <repo-url>
cd phishing-detector
python3 -m venv venv
source venv/bin/activate
pip install flask requests
python3 app.py
