#!/usr/bin/env python

import psycopg2
import datetime

DBNAME = 'news';
#1. What are the most popular three articles of all time?
query1 = '''select * from popular_articles Limit 3;'''

#2. Who are the most popular article authors of all time?
query2= '''select a.name , v.views from authors a, author_rank v 
where a.id = v.author;'''

#3. On which days did more than 1% of requests lead to errors? 
query3 = '''select  e.date , round(e.err_num * 100 /a.num,2) as percent 
from error_logs e ,  all_logs a
where e.date = a.date
and e.err_num > a.num/100
order by percent desc;'''


def connect_to_db(query):
      db = psycopg2.connect(database=DBNAME)
      c = db.cursor()
      c.execute(query)
      results = c.fetchall()
      db.close()
      return results

def most_pop_articles(query):
    results = connect_to_db(query)
    print('The most popular three articles are :')
    for i in results:
        print(i[0]+"\" - "+ str(i[1])+" views")

def most_pop_authors(query):
    results = connect_to_db(query)
    print("The most popular authors are :")
    for i in results:
        print(i[0]+" - "+ str(i[1])+" views")

def error_days(query):
    results = connect_to_db(query)
    print("Days did more than 1% of requests lead to errors are :")
    for i in results:
        print(datetime.datetime.strptime(str(i[0]), '%Y-%m-%d').strftime('%d-%b-%Y')+" - "+ str(i[1])+"% errors") 

if __name__ == '__main__':
	# Print results

    most_pop_articles(query1)
    most_pop_authors(query2)
    error_days(query3)
