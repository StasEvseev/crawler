from grab import Grab, DataNotFound
from collections import namedtuple
import math


class Yandex(object):

    def __init__(self):
        self._g = Grab()
        self._url = 'http://yandex.ru/yandsearch'
        self._sep_params = '?'
        self._sep_prm = '&'
        self._serp_block_class = 'serp-block'
        self._serp_item_class = 'serp-item'
        self.MAX_ITEMS_TO_PAGE = 10

    def create_request(self, query, region_id, page=0):
        req = self._url + self._sep_params + (self._sep_prm.join([
            'lr=' + region_id,
            'text=' + query,
            'p=' + str(page)
        ]))
        return req

    #for-testing
    def fetch_data_local(self):
        self._g.fake_response(open('2.html').read())

    def fetch_data(self, req):
        self._g.go(req)

    def get_serp(self, query, deep, region_id):
        items = self._get_items(deep, query, region_id)

        result = {'positions': [], 'totalResults': '', 'reask_phrase': ''}

        for en, item in enumerate(items):
            result['positions'].append({
                'positions': en,
                'url': item.url,
                'title': item.title,
                'mimeType': item.mime,
                'snippet': item.snippet
            })

        result['totalResults'] = self._get_total()
        result['reask_phrase'] = self._get_reask()

        return result

    def _get_item(self, item):
        full_path_url_title = self.__query_path_url_title(item)
        full_path_snippet = self.__query_path_snippet(item)
        full_path_mime = self.__query_path_mime(item)

        urltitle = self._g.doc.select(full_path_url_title)

        url = urltitle.attr('href')
        title = urltitle.text()
        try:
            snippet = self._g.doc.select(full_path_snippet).text()
        except DataNotFound:
            snippet = ''

        try:
            mime = self._g.doc.select(full_path_mime).attr('alt')
        except DataNotFound:
            mime = 'html'

        return ItemSerp(url=url, title=title, snippet=snippet, mime=mime)

    def _get_items(self, deep, query, region):
        result = []
        if deep != 0:
            count_page = int(math.ceil(float(deep) / self.MAX_ITEMS_TO_PAGE))
            for page in xrange(count_page):
                req = self.create_request(query, region, page)
                self.fetch_data(req)
                if page == count_page - 1 and page != 0:
                    count_items = deep % self.MAX_ITEMS_TO_PAGE + 1
                else:
                    count_items = self.MAX_ITEMS_TO_PAGE + 1
                for item in xrange(1, count_items):
                    result.append(self._get_item(item))
        return result

    def _get_total(self):
        query_count = self.__full_xpath([
            self.__factory_xpath('div', 'input__found')
        ])
        return self._g.doc.select(query_count).text()[2:]

    def _get_reask(self):
        query_misspell = self.__full_xpath([
            self.__factory_xpath('div', 'misspell'),
            self.__factory_xpath('div', 'message'),
            self.__factory_xpath('div', 'misspell__message')
        ])
        try:
            result = self._g.doc.select(query_misspell).text()
        except DataNotFound:
            result = ''
        return result

    def __query_to_serp_item_wrap(self, item):
            query_serp_block = self.__factory_xpath('div', self._serp_block_class)
            query_serp_block_item = self.__factory_xpath('div', self._serp_item_class, item)
            query_serp_item_wrap = self.__factory_xpath('div', 'serp-item__wrap')
            return '/'.join([
                query_serp_block,
                query_serp_block_item,
                query_serp_item_wrap
            ])

    def __query_path_url_title(self, item):
        query_serp_item_wrap = self.__query_to_serp_item_wrap(item)
        query_serp_title = '/'.join([
            self.__factory_xpath('h2', 'serp-item__title'),
            self.__factory_xpath('a', 'b-link serp-item__title-link')])

        return self.__full_xpath([
            query_serp_item_wrap,
            query_serp_title
        ])

    def __query_path_snippet(self, item):
        query_serp_item_wrap = self.__query_to_serp_item_wrap(item)
        query_serp_snippet = self.__factory_xpath('div', 'serp-item__text')

        return self.__full_xpath([
            query_serp_item_wrap,
            query_serp_snippet
        ])

    def __query_path_mime(self, item):
        query_serp_item_wrap = self.__query_to_serp_item_wrap(item)
        query_serp_item_extra_mine = '/'.join([
            self.__factory_xpath('div', 'serp-item__extra-wrap'),
            self.__factory_xpath('div', 'serp-item__extra'),
            self.__factory_xpath('a', 'b-link'),
            self.__factory_xpath('div', 'serp-item__mime'),
            self.__factory_xpath('img', 'serp-item__mime-icon'),
        ])

        return self.__full_xpath([
            query_serp_item_wrap, query_serp_item_extra_mine
        ])

    @classmethod
    def __full_xpath(cls, xpaths):
            first = xpaths[0]
            return '/'.join(['//' + first] + xpaths[1:])

    @classmethod
    def __factory_xpath(cls, tag, clas, index=None):
        index = '[' + str(index) + ']' if index else ''
        return '{0}{1}[contains(@class, "{2}")]'.format(tag, index, clas)


ItemSerp = namedtuple('ItemSerp', ['url', 'title', 'snippet', 'mime'])