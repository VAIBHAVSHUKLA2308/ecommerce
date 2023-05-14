from dputils.scrape import Scraper, Tag
import pandas as pd

class MyScraperGrid:
    def __init__(self, query, page=1):
        self.query = query
        self.page = page
        self.url = f'https://www.flipkart.com/search?q={query}&page={page}'
        self.dataset = []

    def collect(self):
        print(f'Collecting page {self.page}...')
        sc = Scraper(self.url)
        target = Tag(cls='_1YokD2 _3Mn1Gg')
        items = Tag(cls='_1xHGtK _373qXS')
        brand = Tag(cls='_2WkVRV')
        title = Tag('a',cls='IRpwTa')
        rating = Tag(cls='_3LWZlK _1BLPMq')
        price = Tag(cls='_30jeq3')
        oprice = Tag(cls='_3I9_wc')
        discount = Tag(cls='_3Ay6Sb')
        out = sc.get_all(target, items, 
                         name=title, 
                         price=price, 
                         rr=rating, 
                         brand=brand,
                         orignal_price=oprice,
                         discount= discount)
        print(">>>LOG>>>")
        print(out)
        print("<<<LOG<<<")
        return out
    
    def collect_all(self, limit=50):
        for i in range(1, limit):
            result = self.collect()
            if len(result) >= 1:
                print("result set", len(result))
                self.dataset.extend(result)
            self.page = i+1
            self.url = f'https://www.flipkart.com/search?q={self.query}&page={self.page}'
            print(self.url)
            
    def save(self, filename):
        df = pd.DataFrame(self.dataset)
        df.dropna(how='all', inplace=True)
        df.to_csv(filename, index=False)


if __name__ == '__main__':
    # create object
    sc = MyScraperGrid('shoes')
    # collect data
    sc.collect_all()
    # save data
    sc.save('shoes.csv')
    