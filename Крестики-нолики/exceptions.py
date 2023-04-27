""" Модуль кастомных исключений """


class NotEmptyPosition(Exception):
    """ Возбуждается при попытке поставить символ в непустую клетку """
    pass


class GameDraw(Exception):
    """ Возбуждается в случае ничьей """
    pass
