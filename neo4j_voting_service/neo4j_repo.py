from typing import List, Tuple
from neo4j_utils import Neo4jConnection

class Neo4jRepository():
    
    def __init__(self, uri, user, pwd):
        try:
            self.conn = Neo4jConnection(uri, user, pwd)
        except Exception as e:
            print("Failed to create Neo4jFunctions:", e)

    def submit_choices(self, user_id: str, choices: dict[str:str])-> Tuple[bool, str]:
        """
        Submit user's selections to db
        
        Args:
            user_id (str): Current user id.
            choices [dict[str:str]]: Dictionary containing questions asked and answer selected
        
        Returns:
            Tuple[bool, str] of (success, message)
        """ 
        try:
            for question, answer in choices.items():
                self.submit_choice(user_id, question, answer)
            return (True, "")
        except Exception as e:
            print("Failed to submit choices:", e)
            return (False, e)

    def submit_choice(self, user_id: str, question: str, choice:str) -> bool:
        q="""
        MERGE (u:User {name: $user_id})
        MERGE (c:Choice {choice: $choice})
        MERGE (q:Question {question: $question})
        MERGE (c)-[:OPTION_OF]->(q)
        MERGE (u)-[:CHOSE]->(c)
        """
        result = self.conn.write(database='votes', query=q, user_id=user_id, question=question, choice=choice)
        return True
