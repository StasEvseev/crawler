from grab import Grab

class Yandex(object):

    def __init__(self):
        self._g = Grab()
        self._url = 'http://yandex.ru/yandsearch'
        self._sep_params = '?'
        self._sep_prm = '&'
        self._serp_block_class = 'serp-block'
        self._serp_item_class = 'serp-item'

    def create_request(self, query, deep, region_id):
        req = self._url + self._sep_params + 'lr=' + region_id + self._sep_prm + 'text=' + query
        return req

    def fetch_data_local(self):
        self._g.fake_response(open('1.html').read())

    def fetch_data(self, req):
        self._g.go(req)

    def get_serp(self, query, deep, region_id):
        req = self.create_request(query, deep, region_id)
        self.fetch_data_local()

        #print self._g.doc.select('//div[contains(@class, "serp-block")]').exists()
        # print self._g.doc.select('//a[contains(@class, "b-link")]').text()
        serp_items = self._g.doc.select('//div[contains(@class, "' + self._serp_block_class + '")]//div[contains(@class, "' + self._serp_item_class + '")]')

        serp_it = self._g.doc.select('//div[contains(@class, "' + self._serp_block_class + '")]//div[contains(@class, "' + self._serp_item_class + '")]//a[contains(@class, "b-link serp-item__title-link")]')#.select('//a[contains(@class, "b-link serp-item__title-link")]')

        print serp_items.count()
        print serp_it.count()

        for it in serp_it:
            print it.text()

        #print serp_items.exists()
        #print serp_items.html()

        #print serp_items[0].html()
        #print serp_items[15].select('//a[contains(@class, "b-link serp-item__title-link")]').text()
        #print serp_items.count()
        #for item in serp_items:
        #    print item.select('//a[contains(@class, "b-link serp-item__title-link")]').html()

        #    pass
            #print item.select('//a[contains(@class, "b-link")]').text()
            #print item.html()
        #print serp_block.select('//div[contains(@class, "' + self._serp_item_class + '")]').html()
        #print list.select('//a[contains(@class, "b-link")]').html()
        #
        #for el in list:
        #    print el.select('//a[contains(@class, "b-link")]').html()