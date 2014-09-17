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

        def full_xpath(xpaths):
            first = xpaths[0]
            return ('/'.join(['//' + first] + xpaths[1:]))

        def factory_xpath(tag, clas, index=None):
            index = '[' + str(index) + ']' if index else ''
            return '{0}{1}[contains(@class, "{2}")]'.format(tag, index, clas)

        for dp in xrange(deep):
            query_serp_block = factory_xpath('div', self._serp_block_class)
            query_serp_block_item = factory_xpath('div', self._serp_item_class, dp + 1)
            query_serp_item_wrap = factory_xpath('div', 'serp-item__wrap')
            query_serp_title = '/'.join([
                factory_xpath('h2', 'serp-item__title'),
                factory_xpath('a', 'b-link serp-item__title-link')])
            query_serp_snippet = factory_xpath('div', 'serp-item__text')

            full_p = full_xpath([
                query_serp_block,
                query_serp_block_item,
                query_serp_item_wrap,
                query_serp_title
            ])

            full_p2 = full_xpath([
                query_serp_block,
                query_serp_block_item,
                query_serp_item_wrap,
                query_serp_snippet
            ])

            urltitle = self._g.doc.select(full_p)

            snippet = self._g.doc.select(full_p2)

            print urltitle.attr('href')
            print urltitle.text()
            print snippet.text()

            print "---------------------------------"

        query_count = full_xpath([
            factory_xpath('div', 'input__found')
        ])
        query_misspell = full_xpath([
            factory_xpath('div', 'misspell'),
            factory_xpath('div', 'message'),
            factory_xpath('div', 'misspell__message')
        ])
        print self._g.doc.select(query_count).text()[2:]
        print self._g.doc.select(query_misspell).text()