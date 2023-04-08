# -*- coding: utf-8 -*-
from random import randint
quotes = ['И ненавидим мы, и любим мы случайно, ничем не жертвуя ни злобе, ни любви,и царствует в душе какой-то холод тайный, когда огонь кипит в крови._Михаил Лермонтов_Дума',
          "Служить бы рад, прислуживаться тошно._Александр Грибоедов._Горе от ума",
          "Часто сквозь видимый миру смех льются невидимые миру слёзы._Николай Гоголь._Мертвые души"]
quotes_split = [i.split("_") for i in quotes]
print(randint(1, 100))
"""
def add_quote(quote, person, work):
    db_sess = db_session.create_session()
    quote = Russian(quote=quote,
                    person=person,
                    work=work)
    db_sess.add(quote)
    db_sess.commit()


for lst in quotes_split:
    quote, person, work = lst
    add_quote(quote, person, work)"""