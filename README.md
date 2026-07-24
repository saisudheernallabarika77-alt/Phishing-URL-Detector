# Phishing URL Detector

A Flask-based web application that analyzes URLs using heuristic pattern matching to detect potential phishing attempts.

**Institution:** KIET Group of Institutions — Department of Computer Science & Engineering (Cybersecurity)
**Tech Stack:** Python, Flask, HTML/CSS
**Server:** http://127.0.0.1:5000

## Overview

This tool checks a submitted URL against 8 phishing indicators and returns a risk score along with a Safe / Suspicious / Phishing verdict.

## Detection Criteria

- IP address used instead of a domain name
- Presence of '@' symbol in the URL
- Use of known URL shortening services
- Excessive number of subdomains
- Suspicious keywords (login, verify, account, secure, etc.)
- Unusually long URLs
- Missing HTTPS
- Multiple hyphens in the domain (common in spoofed domains)

## How It Works

1. User submits a URL through the web form
2. The Flask backend parses the URL and runs it through each detection rule
3. A cumulative risk score determines the final verdict
4. Results are displayed with the specific reasons behind the score

## Running Locally

```bash
pip install flask requests
python3 app.py# Phishing-URL-Detector
A Flask-based phidhing URL detection tool
