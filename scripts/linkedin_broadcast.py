"""
GitHub-to-LinkedIn Automated Synchronizer & Broadcaster
Publishes latest engineering milestones and project updates to LinkedIn.
"""
import os
import sys
import json
import requests

def get_latest_github_highlights():
    user = "PIYUSH0-7"
    url = f"https://api.github.com/users/{user}/repos?sort=updated&per_page=5"
    headers = {"User-Agent": "GitHub-LinkedIn-Sync"}
    
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return "Building scalable software systems & AI pipelines."
        
    repos = r.json()
    highlights = []
    for repo in repos:
        name = repo.get("name")
        desc = repo.get("description") or "Production engineering repository"
        lang = repo.get("language") or "Full-Stack"
        highlights.append(f"• {name} ({lang}): {desc}")
        
    return "\n".join(highlights)

def main():
    print("🚀 Preparing LinkedIn Engineering Update from GitHub...")
    highlights = get_latest_github_highlights()
    
    post_text = f"""🚀 Engineering Dispatch & Architecture Update

Over on my GitHub, I've curated our software ecosystem into production enterprise monorepos and multi-tenant architectures:

{highlights}

🎯 Key Focus Areas:
⚡ High-Throughput APIs (FastAPI + Next.js 15 + React 19)
🤖 Agentic AI & Vector RAG Pipelines (Google Gemini API)
📦 Enterprise Monorepo Strategy & TypeScript Strict Typing
💡 Algorithmic Rigor & Mathematical DSA in Python

Explore the live architecture on GitHub:
👉 https://github.com/PIYUSH0-7

#SoftwareEngineering #WebDevelopment #FastAPI #NextJS #TypeScript #OpenSource #FullStack #AI
"""
    print("Generated LinkedIn Post:\n")
    print(post_text)
    
    # Check if LinkedIn tokens/cookies are provided for direct dispatch
    li_at = os.environ.get("LINKEDIN_LI_AT")
    jsessionid = os.environ.get("LINKEDIN_JSESSIONID")
    
    if li_at and jsessionid:
        print("[+] Attempting automated LinkedIn publication...")
        # Publication logic via Playwright headless
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                context.add_cookies([
                    {'name': 'li_at', 'value': li_at, 'domain': '.linkedin.com', 'path': '/'},
                    {'name': 'JSESSIONID', 'value': jsessionid, 'domain': '.linkedin.com', 'path': '/'}
                ])
                page = context.new_page()
                page.goto("https://www.linkedin.com/feed/", timeout=30000)
                page.wait_for_timeout(3000)
                
                page.click("button:has-text('Start a post')", timeout=10000)
                page.wait_for_timeout(2000)
                page.fill("div.ql-editor[contenteditable='true']", post_text)
                page.wait_for_timeout(2000)
                page.click("button:has-text('Post')", timeout=10000)
                page.wait_for_timeout(4000)
                
                print("✅ Successfully published engineering update to LinkedIn!")
                browser.close()
        except Exception as e:
            print(f"[-] LinkedIn auto-publish notice: {e}")
    else:
        print("ℹ️ Set LINKEDIN_LI_AT and LINKEDIN_JSESSIONID secrets in GitHub repository to enable 100% automated posting.")

if __name__ == "__main__":
    main()