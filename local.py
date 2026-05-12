from PlaywrightAssistant import PlaywrightAssistantClass
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time, csv, os


class HandWorker(PlaywrightAssistantClass):

    def __init__(self):
        super().__init__()

    def clean_text(self, text):
        return (
            text.replace('\xa0', ' ')
                .replace('\n', ' ')
                .strip()
        )

    def exptract_data_points(self, listing_link, search_category):

        data = {
            "search_category": search_category,
            "title": "",
            "tagline": "",
            "rating": "",
            "no_of_reviews": "",
            "address": "",
            "Telephone": "",
            "Mobile": "",
            "Whatsapp": "",
            "Fax": "",
            "website": "",
            "Email": "",
            "social_links": "",
            "description": "",
            "working_hours": "",
            "languages_spoken": "",
            "services_offer": "",
            "terms_of_payment": "",
            "categories": "",
            "logo": "",
            "images": "",
            "listing_url": listing_link
        }

        try:

            time.sleep(1)

            self.click_on_btn('//button[@data-testid="description-read-more"]', timeout=3000)

            data["title"] = self.extract_single_element('//h1[@data-cy="header-title"]', timeout=3000).strip()
            data["tagline"] = self.extract_single_element('//div[@class="j6"]/h2', timeout=3000).strip()
            data["rating"] = self.extract_single_element('//div[@data-testid="ratings-stars-section"]//span[@data-testid="average-rating"]').strip()
            data["no_of_reviews"] = self.extract_single_element('//span[@data-testid="counter-rating"]').strip()
            data["address"] = self.extract_single_element('//div[span[contains(text(), "Address")]]//button/span').replace('\n', ' ').strip()
            data["Telephone"] = self.extract_single_element('//li[span[contains(text(), "Telephone")]]//a').strip()
            data["Mobile"] = self.extract_single_element('//li[span[contains(text(), "Mobile")]]//a').strip()
            data["Whatsapp"] = self.extract_single_element('//li[span[contains(text(), "WhatsApp")]]//a').strip()
            data["Fax"] = self.extract_single_element('//li[span[contains(text(), "Fax")]]//a').strip()
            data["website"] = self.extract_single_element('//li[span[contains(text(), "Website")]]//a', attr='href')
            data["Email"] = self.extract_single_element('//li[span[contains(text(), "E-Mail")]]//a', attr='href').replace('mailto:', '').strip()
            data["social_links"] = ', '.join(self.extract_multiple_elements('//div[@class="sX"]/a', attr='href'))
            data["description"] = self.extract_single_element('//div[@data-testid="description-content"]').strip()
            data["working_hours"] = self.clean_text(', '.join(self.extract_multiple_elements('(//div[@class="oB notOnMobile"]//ol)[1]/li')))
            data["languages_spoken"] = self.clean_text(', '.join(self.extract_multiple_elements('//preceding-sibling::h3[contains(text(), "Language")]/following-sibling::*[1]')))
            data["services_offer"] = self.clean_text(', '.join(self.extract_multiple_elements('//preceding-sibling::h3[contains(text(), "Offer")]/following-sibling::*[1]/span')))
            data["terms_of_payment"] = self.clean_text(', '.join(self.extract_multiple_elements('//preceding-sibling::h3[contains(text(), "Terms of payment")]/following-sibling::*[1]/span')))
            data["categories"] = self.clean_text(', '.join(self.extract_multiple_elements('//preceding-sibling::dt[contains(text(), "Categories")]/following-sibling::*[1]/a')))
            data["logo"] = self.extract_single_element('//picture/img[contains(@alt, "logo")]', attr='src')
            data["images"] = ', '.join(self.extract_multiple_elements('//button[@aria-label="Click to enlarge"]//img', attr='src'))

        except Exception as e:
            print("Extraction error:", listing_link, e)

        return data


def main(th_num, keyword, input_path):

    results = []

    with open(input_path, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            results.append(row)

    bot = HandWorker()

    for id, d in enumerate(results, start=1):

        try:

            bot.navigate_with_zoomout(d['Link'])

            data_got = bot.exptract_data_points(d['Link'], d['title'])

            print(f"Thread {th_num}: {id}/{len(results)}")

            p = pd.DataFrame([data_got])

            file_path = f"./results/{keyword}-{th_num}.csv"

            p.to_csv(
                file_path,
                mode='a',
                index=False,
                header=not os.path.exists(file_path),
                encoding='utf-8-sig'
            )

        except Exception as e:
            print("Thread error:", e)


if __name__ == "__main__":

    keyword = "metal-and-steel-construction"

    files = [
        f"./{keyword}/1.csv",
        f"./{keyword}/2.csv",
        f"./{keyword}/3.csv",
        f"./{keyword}/4.csv",
        f"./{keyword}/5.csv",
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        for i, file in enumerate(files, start=1):
            executor.submit(main, i, keyword, file)
