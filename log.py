#! /usr/bin/env python3

"""Python program to generate report from the logs generated 
   by a newspaper website"""

import psycopg2


def connect():
    """Method to connect to news database"""  
    return psycopg2.connect("dbname=news")

query1 = """SELECT a.title, top_three_views.views FROM
          articles a,
          (SELECT path, count(*) AS views FROM log
          WHERE status = '200 OK'
          AND path LIKE '/article/%'
          GROUP BY path
          ORDER BY views DESC
          LIMIT 3) as top_three_views
          WHERE '/article/' || a.slug = top_three_views.path
          ORDER BY top_three_views.views DESC"""

query2 = """SELECT auth.name, auth_art_stats.arts_by_auth FROM
          authors auth,
          (SELECT a.author, count(*) AS arts_by_auth
          FROM log l, articles a
          WHERE l.path = '/article/' || a.slug
          GROUP BY a.author
          ORDER BY arts_by_auth DESC) AS auth_art_stats
          WHERE auth.id = auth_art_stats.author"""

query3 = """SELECT time_as_date, err FROM percentage_error WHERE err > 1.0"""


def article_popularity(query1):
    """Method giving the top 3 popular articles"""
    db = connect()
    cur = db.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    for i in range(len(results)):
        title = results[i][0]
        views = results[i][1]
        print("%s--%d" % (title, views))
    db.close()


def author_popularity(query2):
    """Method giving the popularity of the authors"""
    db = connect()
    cur = db.cursor()
    cur.execute(query2)
    results = cur.fetchall()
    for i in range(len(results)):
        name = results[i][0]
        views = results[i][1]
        print("%s--%d" % (name, views))
    db.close()


def percent_error(query3):
    """Method to calclulate percent of bad requests greater than 1"""    
    db = connect()
    cur = db.cursor()
    cur.execute(query3)
    results = cur.fetchall()
    for i in range(len(results)):
        date = results[i][0]
        err_prc = results[i][1]
        print("%s--%.1f %%" % (date, err_prc))

if __name__ == "__main__":
    print("THE LIST OF POPULAR ARTICLES ARE:")
    article_popularity(query1)
    print("\n")
    print("THE LIST OF POPULAR AUTHORS ARE:")
    author_popularity(query2)
    print("\n")
    print("PERC ERROR MORE THAN 1.0:")
    percent_error(query3)
