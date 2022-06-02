from typing import List, Tuple
from neo4j_utils import Neo4jConnection

class Neo4jRepository():
    
    def __init__(self, uri, user, pwd):
        try:
            self.conn = Neo4jConnection(uri, user, pwd)
        except Exception as e:
            print("Failed to create Neo4jFunctions:", e)

    def submit_choices(self, user_id: str, choices: List[str])-> Tuple[bool, str]:
        try:
            for choice in choices:
                self.submit_choice(user_id, choice)
            return (True, "")
        except Exception as e:
            print("Failed to submit choices:", e)
            return (False, e)

    def submit_choice(self, user_id: str, choice:str) -> bool:
        q="""
        MERGE (u:User {id: $user_id})
        MERGE (c:Choice {choice: $choice})
        MERGE (u)-[:CHOSE]->(c)
        """
        result = self.conn.write(database='votes', query=q, user_id=user_id, choice=choice)
        print(f'submit_choice result: {result}')
        return True
