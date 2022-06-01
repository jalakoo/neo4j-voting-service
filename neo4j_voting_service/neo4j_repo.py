from typing import List, Tuple
from neo4j_utils import Neo4jConnection

class Neo4jRepository():
    
    def __init__(self, uri, user, pwd):
        try:
            self.conn = Neo4jConnection(uri, user, pwd)
        except Exception as e:
            print("Failed to create Neo4jFunctions:", e)

    def get_choices(self, uuid: str) -> List[str] :
        assert 'get_choices not implemented'
        return []

    def submit_choice(self, question:str , choice:str) -> bool:
        assert 'submit_choice not implemented'
        return False