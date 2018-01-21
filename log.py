#! /usr/bin/env
#PROJECT:-LOG ANALYSIS
import psycopg2
#import time
def connect():
    return psycopg2.connect("dbname=news")

query1="""select a.title, top_three_views.views from 
          articles a,  
          (select path, count(*) as views from log
          where status = '200 OK'
          and path like '/article/%'
          group by path
          order by views desc
          limit 3) as top_three_views
          where '/article/' || a.slug = top_three_views.path
          order by top_three_views.views desc"""

query2="""select auth.name, auth_art_stats.arts_by_auth from 
          authors auth, 
          (select a.author, count(*) as arts_by_auth
          from log l, articles a
          where l.path = '/article/' || a.slug
          group by a.author
          order by arts_by_auth desc) as auth_art_stats
          where auth.id = auth_art_stats.author"""

query3="""select time_as_date, err from percentage_error where err > 1.0"""

def article_popularity(query1):
    db=connect()
    cur=db.cursor()
    cur.execute(query1)
    results=cur.fetchall()
    for i in range(len(results)):
        title=results[i][0]
        views=results[i][1]
        print("%s--%d" % (title,views))
    db.close()

def author_popularity(query2):
    db=connect() 
    cur=db.cursor()
    cur.execute(query2)
    results=cur.fetchall()
    for i in range(len(results)):
        name=results[i][0]
        views=results[i][1]
        print("%s--%d" % (name,views))
    db.close()

def percent_error(query3):
    db=connect()
    cur=db.cursor()
    cur.execute(query3)
    results=cur.fetchall()
    for i in range(len(results)):
        date=results[i][0]
        err_prc=results[i][1]
        print("%s--%.1f %%" %(date,err_prc))

if __name__ == "__main__":
  print("THE LIST OF POPULAR ARTICLES ARE:")
  article_popularity(query1)
  print("\n")
  print("THE LIST OF POPULAR AUTHORS ARE:")
  author_popularity(query2)
  print("\n")
  print("PERC ERROR MORE THAN 1.0:")
  percent_error(query3)