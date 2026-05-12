from PlaywrightAssistant import PlaywrightAssistantClass
import time, pandas, os, threading


class LocalCHLinks(PlaywrightAssistantClass):
    def __init__(self):
        PlaywrightAssistantClass.__init__(self)

    def extract_city_links(self):
        links = {}
        city_links = self.page.locator('//a[@class="cH dv"]').all()
        for city in city_links:
            links[city.inner_text(timeout=1000)] = "https://www.local.ch" + city.get_attribute('href', timeout=1000)
        return links
    
    def extract_page_links(self):
        page_links = self.extract_multiple_elements(selector='//a[@class="lD"]', attr='href', timeout=5000)
        page_links = ["https://www.local.ch" + page for page in page_links]
        return page_links
    


def main(keyword, main_url):
    bot = LocalCHLinks()
    bot.navigate_with_zoomout(main_url)
    cites = bot.extract_city_links()
    for k, v in cites.items():
        data_links = []
        bot.navigate(v)
        print(f"Extract links from: {k}.....")
        while True:
            links = bot.extract_page_links()
            for l in links:
                data_links.append(l)
            try:
                next_btn = bot.page.locator('//div[@id="scrollMapBtnContainer"]//button[span[text() = "Next"] and not(@disabled)]').nth(0)
                next_btn.scroll_into_view_if_needed(timeout=2000)
                time.sleep(1)
                next_btn.click(force=True, timeout=2000)
                time.sleep(1)
            except Exception as e:
                print(e)
                break
        for d in data_links:
            p = pandas.DataFrame([{"title": k , "Link": d}])
            p.to_csv(f"./links/{keyword}.csv", mode='a', header=not os.path.exists(f"./links/{keyword}.csv"), index=False)
        else:
            data_links.clear()


th1 = threading.Thread(target=main, args=("plasterer", "https://www.local.ch/en/categories/p/plasterer", ))
th1.start()
time.sleep(5)

th2 = threading.Thread(target=main, args=("floor-coverings-wall-coverings", "https://www.local.ch/en/categories/f/floor-coverings-wall-coverings", ))
th2.start()
time.sleep(5)

th3 = threading.Thread(target=main, args=("metal-and-steel-construction", "https://www.local.ch/en/categories/m/metal-and-steel-construction", ))
th3.start()


th1.join()
th2.join()
th3.join()

