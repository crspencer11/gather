import requests
from bs4 import BeautifulSoup

url = 'https://coinmarketcap.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Example: Get all the titles of cryptocurrencies listed on the first page
# for row in soup.find_all('tr'):
#     name = row.find('p', class_='coin-item-symbol')
#     if name:
#         print(name.text)

def find_last_page() -> int:
    """
    Finds last page number from HTML webpage. this is to set Loop threshold for later processing.
    """
    page_items = soup.find_all('a', attrs={'aria-label': True})
    if len(page_items) >= 2:
        end_page = page_items[-2]
        last_page_number = int(end_page.text)
        print("Last page number:", last_page_number)
    else:
        print("No page numbers found.")
    return last_page_number