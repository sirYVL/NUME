# earlybird.py
import requests
import smtplib
import time
from email.message import EmailMessage

# --- CONFIGURATION ---
GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
SEARCH_KEYWORD = "AI"  # <-- you can replace this dynamically later
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password_or_app_password"
TO_EMAIL = "recipient_email@example.com"

# For Gmail users, you might need an App Password if 2FA is on.

# --- FUNCTION ---
def search_github_repos(keyword):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "q": f"{keyword} in:name",
        "sort": "updated",
        "order": "desc",
        "per_page": 5
    }
    response = requests.get("https://api.github.com/search/repositories", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print("GitHub API error:", response.status_code)
        return []

def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# --- MEMORY ---
already_seen = set()

# --- MAIN LOOP ---
while True:
    print("Checking GitHub...")
    repos = search_github_repos(SEARCH_KEYWORD)
    new_repos = []

    for repo in repos:
        if repo["id"] not in already_seen:
            already_seen.add(repo["id"])
            new_repos.append(f'{repo["name"]} - {repo["html_url"]}')

    if new_repos:
        body = "New GitHub repositories:\n\n" + "\n".join(new_repos)
        send_email("🚀 New GitHub Repos Matching: " + SEARCH_KEYWORD, body)
        print(f"Found {len(new_repos)} new repos! Email sent.")
    else:
        print("No new repos.")

    time.sleep(3600)  # Wait 1 hour between checks
