
import requests as rq
import pandas as pd
import argparse
import re


url_regex = re.compile(r'^https?://', re.IGNORECASE)


class FetchProducts:
    """
    Docs
    """

    def __init__(self, store_domain: str) -> None:
        global url_regex
        if url_regex.match(store_domain):
            print('Valid Store Domain')
        else:
            raise ValueError("Invalid Store Domain")
        filename = store_domain.split('.')[1]
        self.path = f'data/{filename}.csv'
        self.products_store = []
        self.store_domain = store_domain

    def filterSaveReturn(self) -> pd.DataFrame:
        if len(self.products_store) < 2:
            raise ValueError('Very few Data!')
        df = pd.DataFrame(self.products_store)
        df['link'] = f'{self.store_domain}/products/' + df['handle']

        df['tags'] = df['tags'].transform(lambda row: ' '.join(row))
        df['summary'] = df['title'] + ' ' + df['tags'] + \
            ' ' + df['product_type'] + ' ' + df['vendor']
        # To Save data
        # df[['id', 'title', 'handle', 'vendor', 'product_type', 'tags', 'link', 'summary']].to_csv(
        #     self.path, index=False)
        # print(f"Data Saved at {self.path}")

        return df[['id', 'title', 'handle', 'vendor', 'product_type', 'tags', 'link', 'summary']]

    def fetch(self) -> None:
        page = 1
        while True:
            source = f'{self.store_domain}/collections/all/products.json'
            resp = rq.get(url=source, params={'page': page})
            if resp.status_code != 200:
                print('Request Unsuccessful')
                break
            data = resp.json()
            if data['products'] == []:
                print('Products Fetched Successfully')
                break
            self.products_store.extend(data['products'])
            print(f'Extracted Page {page} | Len {len(self.products_store)}')
            page += 1

    def run(self) -> None:
        self.fetch()
        return self.filterSaveReturn()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'store_domain', help='The domain of the store: https://www.boysnextdoor-apparel.co')
    args = parser.parse_args()

    # get Products
    spider = FetchProducts(store_domain=args.store_domain)
    spider.run()
