from models.basic import *

cmc = 'https://coinmarketcap.com/'
obj = DataSource(cmc)
obj.gather_data()