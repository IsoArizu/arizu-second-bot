from data.parser.parser import parse
import random

sorted_categories = {"Hentai": ["Anime Ero", "Этти", "Boobs", "Ass"],
                     "Anime": ["Animal Ears", "Anime Cosplay", "Anime Няши"],
                     "Art": ["Anime Комиксы", "Anime Гифки", "Manga"]}

titles = {'Anime Ero': '/tag/Anime+Ero',
          'Этти': "/tag/ecchi",
          'Animal Ears': '/tag/Animal+Ears',
          'Anime Комиксы': '/tag/Anime+%D0%9A%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B',
          'Anime Гифки': '/tag/Anime+%D0%93%D0%B8%D1%84%D0%BA%D0%B8',
          'Anime Cosplay': '/tag/Anime+Cosplay',
          'Anime Няши': '/tag/Anime+%D0%9D%D1%8F%D1%88%D0%B8',
          'Manga': '/tag/Manga',
          "Ass": "/tag/oshiri",
          "Boobs": "/tag/Anime+Ero+Oppai"}

Categories = [i for i in titles]


class CategoryNameError(Exception):
    pass


def check_name(name):
    if name in Categories:
        return titles[name]
    else:
        raise CategoryNameError()


def get_name():
    r = random.choice(Categories)
    return titles[r]


def purse_func(name):
    pos = random.randint(1, 10)
    page = random.randint(1, 20)
    arg1, arg2 = parse(name, pos, page)
    return arg1, arg2
