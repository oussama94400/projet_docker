#!/usr/bin/env python3

import logging

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "testkeyspace"


def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    log.info("creating keyspace...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    log.info("creating table...")
    session.execute("""create table testkeyspace.test (film text PRIMARY KEY, genres text ,studio text,audience text,profie text ,note text, prix text,annee text)""") 


   

    #query = SimpleStatement("""
     #   INSERT INTO mytable (thekey, col1, col2)
     #   VALUES (%(key)s, %(a)s, %(b)s)
      #  """, consistency_level=ConsistencyLevel.ONE)

    #prepared = session.prepare("""
     #   INSERT INTO mytable (thekey, col1, col2)
      #  VALUES (?, ?, ?)
      #  """)

    #for i in range(10):
    #    log.info("inserting row %d" % i)
    #    session.execute(query, dict(key="key%d" % i, a='a', b='b'))
     #   session.execute(prepared, ("key%d" % i, 'b', 'b'))

    future = session.execute_async("SELECT * FROM mytable")


    try:
        rows = future.result()
    except Exception:
        log.exception("Error reading rows:")
        return

    for row in rows:
        log.info('\t'.join(row))

    #session.execute("DROP KEYSPACE " + KEYSPACE)
    
    prepared = session.prepare("""INSERT INTO testkeyspace.test (film, genres, studio, audience, profie, note, prix, annee)VALUES (?, ?, ?, ?, ?, ?, ?, ?)""")
    
    with open("movies.csv", "r") as fares:
        for fare in fares:
            columns=fare.split(",")
            film=columns[0]
            genres=columns[1]
            studio=columns[2]
            audience=columns[3]
            profie=columns[4]
            note=columns[5]
            prix=columns[6]
            annee=columns[7]
            session.execute(prepared, [film,genres,studio,audience,profie,note,prix,annee])
        fares.close()
    #closing Cassandra connection
    session.shutdown()

if __name__ == "__main__":
    main()
