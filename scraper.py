from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep

class Scraper():

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.category_list = []
        self.product_dict = {}

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
    
    def get_product_links(self):
        '''
        first pass/crawl to retrieve a list of products by crawling through product list pages by category
        this category data is unretrieveable from the individual product pages so much be compiled from 'collection' pages
        '''
        self.product_links = {}
        for url in self.category_list:

            self.get(url)
            self.show_more()
            products = self.driver.find_elements(By.XPATH, '//div[contains(@class,"product-grid")]/div/div[contains(@class,"product")]')
            url_list = [x.find_element(By.XPATH, './div/a').get_attribute('href').split('?')[0] for x in products]
            self.product_links[url] = url_list

        
        return

    def get_category_links(self):
        '''
        get list of category urls, used for crawling to get product urls
        '''
        navbar = self.wait_for_element((By.XPATH,'//ul[contains(@class,"navbar-nav")]'),10)
        categories = navbar.find_elements(By.XPATH, './li[contains(@class, "nav-item-cat")]/a')
        unchecked_category_urls = [x.get_attribute('href').split('?')[0] for x in categories]
        category_urls = []
        while True:
            if not unchecked_category_urls:
                break
            url = unchecked_category_urls.pop()
            if url in category_urls:
                continue
            category_urls.append(url)
            try:
                self.get(url)
                refinement_slider = self.wait_for_element((By.XPATH,'//div[@class="refinement-container"]'),10)
                refinement_category_urls = [x.get_attribute('href').split('?')[0] for x in refinement_slider.find_elements(By.XPATH, './/div[contains(@class,"tns-inner")]//a')]
                unchecked_category_urls.extend(refinement_category_urls)
            except Exception:
                pass
        self.category_list = category_urls
        return self.category_list


    def show_more(self):
        '''
        general method to populate more products on catalogue/collection page, should fail gracefully if page is fully populated
        '''
        while True:
            try:
                more_button = self.wait_for_element((By.XPATH,'//div[@class="show-more"]//button'), 10)
                more_button.click()
                sleep(1)
            except AttributeError:
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
    pop_scraper.decline_voucher()
    pop_scraper.get_category_links()
    #pop_scraper.category_list = [ 'https://www.popsockets.co.uk/en-gb/popculture', 'https://www.popsockets.co.uk/en-gb/popculture/friends']  #['https://popsockets-promo.eu/', 'https://www.popsockets.co.uk/en-gb/popculture', 'https://www.popsockets.co.uk/en-gb/popculture/friends', 'https://www.popsockets.co.uk/en-gb/popculture/dc-comics', 'https://www.popsockets.co.uk/en-gb/popculture/star-wars', 'https://www.popsockets.co.uk/en-gb/popculture/star-wars/the-mandalorian', 'https://www.popsockets.co.uk/en-gb/popculture/star-wars/obi-wan-kenobi', 'https://www.popsockets.co.uk/en-gb/popculture/marvel', 'https://www.popsockets.co.uk/en-gb/popculture/disney', 'https://www.popsockets.co.uk/en-gb/popculture/disney/pixar', 'https://www.popsockets.co.uk/en-gb/popculture/disney/the-nightmare-before-christmas', 'https://www.popsockets.co.uk/en-gb/popculture/disney/mickey-and-minnie', 'https://www.popsockets.co.uk/en-gb/popculture/disney/lilo-and-stitch', 'https://www.popsockets.co.uk/en-gb/popculture/harry-potter', 'https://www.popsockets.co.uk/en-gb/popculture/all-popculture', 'https://www.popsockets.co.uk/en-gb/new']
    
    pop_scraper.get_product_links()

