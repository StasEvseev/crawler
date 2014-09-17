#coding: utf-8

from yandex import Yandex
from grab import Grab

def main():

    # data = open('1.html').read()
    # g = Grab(data)

    # g = Grab(charset='utf-8')
    # g.go('http://yandex.ru/yandsearch?lr=213&text=test')


    # if g.xpath_text('//title') == u'Ой!':
    #     a = u"НАСТЯ"
    #     print g.xpath('//img[@class="b-captcha__image"]').get('src')
    #     g.set_input("rep", a)
    #     resp = g.submit()
    #     print resp.body
    ya = Yandex()
    ya.get_serp('test', 10, '213')
    # print g.xpath_text('//title')
    # print g.response.body



    # g.go('http://habrahabr.ru')
    # print g.xpath('//h2/a[@class="topic"]').get('href')
    # print g.xpath_text('//title')

    # print g.doc.select('//div[contains(@class, "serp-block")]').exists()



if __name__ == "__main__":
    main()