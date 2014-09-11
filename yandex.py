from grab import Grab

class Yandex(object):

    def __init__(self):
        self._g = Grab()
        self._url = 'http://yandex.ru/yandsearch'
        self._sep_params = '?'
        self._sep_prm = '&'
        self._serp_block_class = 'serp-block'

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

        print self._g.doc.select('//div[contains(@class, "serp-block")]').exists()
        # print self._g.doc.select('//a[contains(@class, "b-link")]').text()
        serp_block = self._g.doc.select('//div[contains(@class, "' + self._serp_block_class + '")]')
        print serp_block.exists()
        list = serp_block.select('//div[contains(@class, "serp-item")]').count()
        print list
        #
        for el in list:
            print el.select('//a[contains(@class, "b-link")]')