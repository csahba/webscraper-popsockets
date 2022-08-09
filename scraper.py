from asyncio import wait_for
from dis import show_code
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep

class Scraper():

    def __init__(self):
        self.driver = webdriver.Chrome()

    def get(self, url):
        self.driver.get(url)
    
    def accept_cookies(self):
        #sleep(5)
        #cookiebutton = self.driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-container"]')
        cookiebutton = self.wait_for_element((By.XPATH, '//*[@id="onetrust-accept-btn-container"]'))
        cookiebutton.click()

    def decline_voucher(self):
        '''
        10% off voucher popup, appears after 30 seconds as best can tell
        '''
        voucherbutton = self.wait_for_element((By.CSS_SELECTOR, 'button.needsclick.klaviyo-close-form'), 40)
        voucherbutton.click()
        
    def wait_for_element(self, locator, delay = 30):
        try:            
            awaitedelement = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(locator))
            print(f'Element {locator[1]} found')
            return awaitedelement
        except TimeoutException:
            print("Element not yet there")
    
    def get_links(self):
        '''
        first pass/crawl to retrieve a list of products by crawling through product list pages by category
        this category data is unretrieveable from the individual product pages so much be compiled from 'collection' pages
        '''
        pass

    def show_more(self):
        '''
        general method to scroll down and populate more products on catalogue/collection page, should fail gracefully if page is fully populated
        '''
        while True:
            try:
                more_button = self.wait_for_element((By.XPATH,'//div[@class="show-more"]//button'), 20)
                more_button.click()
            except Exception:
                print('Element cannot be clicked')
                break

    def scrape_product_page(self):
        '''
        second pass/scraping from individual product page for price, review rating, description text
        '''
        pass
        

if __name__ == '__main__':
    pop_scraper = Scraper()
    pop_scraper.get('https://www.popsockets.co.uk/')
    pop_scraper.accept_cookies()
    #pop_scraper.decline_voucher()
    pop_scraper.get('https://www.popsockets.co.uk/en-gb/search?cgid=root')
    pop_scraper.show_more()

