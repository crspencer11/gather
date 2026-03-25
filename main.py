import requests
from bs4 import BeautifulSoup

home = 'https://coinmarketcap.com/'
home_page = requests.get(home)
soup = BeautifulSoup(home_page.text, 'html.parser')

# Example: Get all the titles of cryptocurrencies listed on the first page
# for row in soup.find_all('tr'):
#     name = row.find('p', class_='coin-item-symbol')
#     if name:
#         print(name.text)

class DataClass:
    def __init__(self, home: str):
        self.home = home
        self.total_pages = self._find_last_page(home)

    @classmethod
    def _find_last_page(page) -> int:
        """
        Finds last page number from HTML webpage. this is to set Loop threshold for later processing.
        """
        page_items = page.find_all('a', attrs={'aria-label': True})
        if len(page_items) >= 2:
            end_page = page_items[-2]
            last_page_number = int(end_page.text)
            print("Last page number:", last_page_number)
        else:
            print("No page numbers found.")
        return last_page_number

    def gather_data(self):
        print("Gathering Data...")
        pages = []
        total_pages = self.find_last_page(home)
        for page_num in range(1, total_pages):
            pages.append(home+"?page="+str(page_num))

        for page in pages:
            print(f"Scrapping data from Page {page}")
