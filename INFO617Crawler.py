## need to import bs4, requests, and pandas with pip install

from bs4 import BeautifulSoup
import requests 
import pandas

## can put in any remax location. need to grab path from website (i.e. https://www.remax.com/homes-for-sale/dc/washington/city/1150000)
## makes initial soup to grab pages for pagination

paginatorUrl = 'https://www.remax.com/homes-for-sale/va/richmond/city/5167000/'
paginatorPage = requests.get(paginatorUrl)

paginatorSoup = BeautifulSoup(paginatorPage.content, 'html.parser')

pages = paginatorSoup.find_all('a', 'd-pagination-page d-pagination-el')[-1].text

## now that we have access to pages, we can paginate over the website to collect all the data

info = []
for i in range (1, int(pages)):

   url = f'https://www.remax.com/homes-for-sale/va/richmond/city/5167000/page-{i}'
   page = requests.get(url)

   soup = BeautifulSoup(page.content, 'html.parser')

   lists = soup.find_all('div', 'listings-card')

   for list in lists:
      address = list.find('a', 'text-grey-darker hover:text-grey-darker').text.replace('\n', '')
      pricing = list.find('h4', 'price').text.replace('\n', '')
      stats = list.find('div', 'card-details-stats').text.replace('\n', '')
      link = 'https://www.remax.com/' + list.find('a', 'text-grey-darker hover:text-grey-darker')['href'].replace('\n', '')
      
      info.append([address, pricing, stats, link])

df = pandas.DataFrame(info, columns=['Address', 'Price', 'Stats', 'Link'])
df.to_csv('ForSale.csv')