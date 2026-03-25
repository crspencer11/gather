import requests
from bs4 import BeautifulSoup
from typing import DefaultDict

class DataSource:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._home_page = self._create_home_page()
        self._total_pages = self._find_last_page()
        self._storage = DefaultDict(list) = {}

    def _create_home_page(self):
        home = requests.get(self.base_url)
        return BeautifulSoup(home.text, 'html.parser')

    def _find_last_page(self) -> int:
        """
        Finds last page number from HTML webpage. this is to set Loop threshold for later processing.
        """
        page_items = self._home_page.find_all('a', attrs={'aria-label': True})
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
        total_pages = self._total_pages
        for page_num in range(1, total_pages):
            pages.append(self.base_url+"?page="+str(page_num))

        for page in pages:
            print(f"Scrapping data from Page {page}")
            current_page = requests.get(page)

    def get_coins(self, page):
        for row in page.find_all('tr'):
            name = row.find('p', class_='coin-item-symbol')
            if name and name not in self._storage:
                print(name.text)
                self._storage[name] = row