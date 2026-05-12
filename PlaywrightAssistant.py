from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from threading import Thread
# import pandas as pd 
import re
import os
import time, pickle


class PlaywrightAssistantClass:
    def __init__(self):
        with open("cookies.pkl", "rb") as cookie:
            cookies = pickle.load(cookie)
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.context.add_cookies(cookies)
        self.page = self.context.new_page()
        stealth_sync(self.page)
        self.links = []

    def navigate(self, url):
        self.page.goto(url, wait_until='networkidle', timeout=60000)
        # self.page.evaluate('document.body.style.zoom="25%"')
    
    def navigate_with_zoomout(self, url):
        self.page.goto(url, wait_until='networkidle', timeout=60000)
        self.page.evaluate('document.body.style.zoom="25%"')

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
    
    def extract_single_element(self, selector, timeout=500, attr='text'):
        try:
            element = self.page.locator(selector).first
            if attr == 'text':
                return element.text_content(timeout=timeout)
            else:
                return element.get_attribute(attr, timeout=timeout)
        except:
            return ""
    
    def extract_multiple_elements(self, selector, timeout=500, attr='text'):
        try:
            elements = self.page.locator(selector).all()
            results = []
            for element in elements:
                if attr == 'text':
                    results.append(element.text_content(timeout=timeout))
                else:
                    results.append(element.get_attribute(attr, timeout=timeout))
            return results
        except Exception as e:
            print(e)
            return []
    
    def click_on_btn(self, selector, timeout=500):
        try:
            element = self.page.locator(selector).first
            element.click(timeout=timeout)
        except:
            print(f"Could not click on button: {selector}")