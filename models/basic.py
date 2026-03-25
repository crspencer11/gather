import requests
from bs4 import BeautifulSoup
from typing import DefaultDict

class DataSource:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._home_page = self._create_home_page()
        self._total_pages = self._find_last_page()
        self._storage =  {}

    def _create_home_page(self) -> BeautifulSoup:
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
        paginated_urls = []
        total_pages = self._total_pages
        for page_num in range(1, total_pages):
            paginated_urls.append(self.base_url+"?page="+str(page_num))

        for page_url in paginated_urls:
            self._get_coins(page_url)

    def _get_coins(self, paginated_url: str):
        print(f"Scrapping data from {paginated_url}")
        page = requests.get(paginated_url)
        html_page = BeautifulSoup(page.text, 'html.parser')
        for row in html_page.find_all('tr'):
            symbol = row.find('span', class_='crypto-symbol')
            name_tag = row.find_all('span')
            name = name_tag[1].text if len(name_tag) > 1 else None
            print(f"Name: {name}, Symbol: {symbol.text if symbol else None}")            # price = row.find('p', class='')
            # if name and name not in self._storage:
            #     self._storage[name] = 