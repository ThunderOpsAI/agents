from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.upwork.com/nx/search/jobs/?q=python"

def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(SEARCH_URL)
        page.wait_for_selector("section")

        jobs = page.query_selector_all("section")

        results = []
        for job in jobs[:10]:
            title = job.query_selector("h4")
            link = job.query_selector("a")

            if title and link:
                results.append({
                    "title": title.inner_text(),
                    "url": "https://www.upwork.com" + link.get_attribute("href")
                })

        browser.close()
        return results


if __name__ == "__main__":
    jobs = scrape()
    for j in jobs:
        print(j)
