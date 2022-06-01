# From https://github.com/cj2001/neo4j_streamlit/edit/main/src/neo4j_utils.py
from neo4j import GraphDatabase

class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(
                self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()


    # This does not work as expected
    def read(self, query, **kwargs):
        assert self.__driver is not None, "Driver not initialized!"
        def execute(tx):
            result = tx.run(query, kwargs)
            return result
        try:
            with self.__driver.session() as session:
                return session.write_transaction(execute)
        except Exception as e:
            print("read failed:", e)

    def write(self, query, **kwargs):
        assert self.__driver is not None, "Driver not initialized!"
        def execute(tx):
            result = tx.run(query, kwargs)
            return result
        try:
            with self.__driver.session() as session:
                return session.write_transaction(execute)
        except Exception as e:
            print("write failed:", e)
