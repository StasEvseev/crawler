#coding: utf-8

from yandex import Yandex


def main():
    ya = Yandex()
    print ya.get_serp('спецификация doc файла', 55, '213')

if __name__ == "__main__":
    main()