from selenium import webdriver
import requests, os

class ImageDownloader:

    def __init__(self) -> None:
        if(not os.path.isdir('images')):
            os.mkdir('images')

    def write_in_file(self, data, image_name):

        path = f'images/{image_name}'
        
        with open(path, 'wb') as f:
            for chunk in data:
                f.write(chunk)

    def download_images(self, links):

        for url in links:
            r = requests.get(url, stream=True)
            print(url, r.status_code)

            if r.status_code == 200:
                image_name =  url.split('/')[-1]
                self.write_in_file(r, image_name)

class Scraper:
    main_url = 'https://pixelz.cc/images/category'
    chromedriver_path = './chromedriver/chromedriver'

    def __get_default_chrome_options(self):

        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')

        return chrome_options

    def check_page_exists(self, url):

        response = requests.get(url)

        if(response.status_code == 200):
            return True

    def run_script(self, categories):

        images_link = []
        for category in categories:

            page_no = 2
            while(page_no <= 100):
                next_page_link = self.main_url + f'/{category}/page/{page_no}'

                page_exists = self.check_page_exists(next_page_link)

                if(page_exists):
                    page_no += 1
                    options = self.__get_default_chrome_options()
                    driver = webdriver.Chrome(self.chromedriver_path, options=options)
                    driver.get(next_page_link)

                    elements = driver.find_elements_by_class_name('dcs_view_details')

                    for item in elements:
                        images_link.append(item.get_attribute('href'))
                else:
                    break

        return images_link

    def get_downloadable_image_link(self, images_link):

        options = self.__get_default_chrome_options()

        driver = webdriver.Chrome(self.chromedriver_path, options=options)

        images_downloadable_link = []
        for url in images_link:
            driver.get(url)
            el = driver.find_element_by_id('main_product_image')
            uri = el.get_attribute('href')
            print(url, uri)
            images_downloadable_link.append(uri)

        driver.close()
        return images_downloadable_link

if __name__ == '__main__':

    total_categories = ['textures-and-backgrounds', 'video-games']

    required_categories = ['nature']

    scraper = Scraper()
    images_link = scraper.run_script(required_categories)
    images_downloadable_link = scraper.get_downloadable_image_link(images_link)

    downloader = ImageDownloader()
    downloader.download_images(images_downloadable_link)