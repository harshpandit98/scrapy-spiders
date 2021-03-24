import requests
import pandas as pd
import asyncio
import nest_asyncio
nest_asyncio.apply()

url = 'https://api.serphouse.com/serp/live'
oneill_url = 'https://www.oneill.com/fr/'
serphouse_key = 'YOUR_SERPHOUSR_KEY'

async def serp_url(queries):
    '''
        Input: Google search codes,
        Output: Url list,
        Serp limit: 200 serps
        Description: A GSC search request to serphouse, if the status is success and search results are not empty, 
                     extract the 1st result of results and appened it to url list. 
    '''
    urls = []
    for query in queries:
        payload = {
            "data": {
                'q': oneill_url + query,
                'domain': 'google.com',
                'lang': 'en',
                'device': 'desktop',
                'serp_type': 'web',
                'loc': 'Alba,Texas,United States',
                'verbatim': '0',
                'page': '1'
            }
        }
        headers = {
            'Authorization': f'Bearer {serphouse_key}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request('POST', url, headers=headers, json=payload)
            data = response.json()
            if data['status'] == 'success':
                if len(data['results']['results']) > 1:
                    
                    prod_url = data['results']['results']['organic'][0]['link']
                    if ('https://www.oneill.com/' in prod_url):
                        print(prod_url)
                        urls.append( tuple( (query , prod_url)))
                    else:
                        print(prod_url)
                        urls.append( tuple((query , f'product url with {oneill_url} domain not found.')))
                else:
                    urls.append( tuple((query , f'No results found.')))
            else:
                print('Status: ',data['status'])
        except Exception as e:
            raise e
    return urls
        
file_name = "data.csv"
df = pd.read_csv(file_name)
google_search_codes = df['Google Search Code']


def generate_urls():
    '''
       Description: stores the urls to csv. 
    '''
    loop = asyncio.get_event_loop()
    urls = loop.run_until_complete(serp_url(google_search_codes))
    df['Product Page URL'] = pd.DataFrame(urls, columns=['gsc','url'])['url']
    df.to_csv('prod_urls.csv')
    return urls
