import requests
from bs4 import BeautifulSoup, Tag
from typing import DefaultDict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

class DataSource:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._home_page = self._create_home_page()
        self._headers = self._extract_headers(self._home_page)
        self._total_pages = self._find_last_page()
        self._storage = {}

    def _create_home_page(self) -> BeautifulSoup:
        home = requests.get(self.base_url)
        return BeautifulSoup(home.text, 'html.parser')

    def _extract_headers(self, soup: BeautifulSoup) -> List[str]:
        headers = []
        header_tags = soup.find_all('p', class_="sc-71024e3e-0 fSsxNG")
        for tag in header_tags:
            headers.append(tag.get_text(strip=True))
        return headers

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
            last_page_number = 1
        return last_page_number

    def gather_data(self):
        print("Gathering Data...")
        paginated_urls = [self.base_url + f"?page={page_num}" for page_num in range(1, self._total_pages + 1)]
        
        def fetch_and_process(page_url):
            page_table = self._get_page_table(page_url)
            self.find_headers(page_table)
            return page_table

        results = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_url = {executor.submit(fetch_and_process, url): url for url in paginated_urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")

    def _get_page_table(self, paginated_url: str) -> Tag:
        page = requests.get(paginated_url)
        html_page = BeautifulSoup(page.text, 'html.parser')
        table = html_page.find('table')
        return table

    def find_headers(self, page_table: Tag):
        headers = page_table.find_all('p', class_="sc-71024e3e-0 fSsxNG")
        for header in headers:
            self._headers.append(header.get_text(strip=True))

    def _get_coins(self, paginated_url: str) -> Tag:
        print(f"Scrapping data from {paginated_url}")
        page = requests.get(paginated_url)
        html_page = BeautifulSoup(page.text, 'html.parser')
        tbody = html_page.find('tbody')
        if tbody:
            print(tbody)
            # for row in tbody.find_all('tr'):
            #     print(row)
                # symbol = row.find('span', class_='crypto-symbol')
                # name_tag = row.find_all('span')
                # name = name_tag[1].text if len(name_tag) > 1 else None
                # print(f"Name: {name}, Symbol: {symbol.text if symbol else None}")            
                # price = row.find('td $')
                # print(price)
                # if name and name not in self._storage:
                #     self._storage[name] =