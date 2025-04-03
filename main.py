
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from playwright.sync_api import sync_playwright
import csv

app = FastAPI()
SCRAPED_FILE = "scraped_data.csv"

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return '''
    <html>
        <head><title>ShopWise Argos Scraper</title></head>
        <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>🛍️ ShopWise Argos Scraper</h1>
            <form action="/run" method="get">
                <button style="padding: 10px 20px; font-size: 16px;">▶️ Run Scraper</button>
            </form><br>
            <a href="/download"><button style="padding: 10px 20px; font-size: 16px;">📥 Download CSV</button></a>
        </body>
    </html>
    '''

@app.get("/run")
def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto("https://www.argos.co.uk/browse/home-and-furniture/c:29351/")
        page.wait_for_timeout(3000)
        links = page.eval_on_selector_all("a", "els => els.map(el => el.href).filter(Boolean)")
        browser.close()

        with open(SCRAPED_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Link"])
            for link in links[:20]:
                writer.writerow([link])
    return HTMLResponse("<h2>✅ Scraping complete. <a href='/'>Go back</a></h2>")

@app.get("/download")
def download_csv():
    return FileResponse(SCRAPED_FILE, media_type='text/csv', filename=SCRAPED_FILE)
