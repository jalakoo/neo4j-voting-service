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
                print(f'submit_choices: question: {question}, answer: {answer}')
                self.submit_choice(user_id, question, answer)
            return (True, "")
        except Exception as e:
            print("Failed to submit choices:", e)
            return (False, e)

    def submit_choice(self, user_id: str, question: str, choice:str) -> bool:
        if question == None or question == "":
            return False
        if choice == None or choice == "":
            return False
        q="""
        MERGE (u:User {name: $user_id})
        MERGE (c:Choice {name: $choice})
        MERGE (q:Question {name: $question})
        MERGE (c)-[:OPTION_OF]->(q)
        MERGE (u)-[:CHOSE]->(c)
        """
        _ = self.conn.write(database='votes', query=q, user_id=user_id, question=question, choice=choice)
        return True

    # def get_all_user_choices(self):
    #     q = """
    #     MATCH (n:User)-[r]->(c:Choice) RETURN n.name as user, c.name as choice
    #     """
    #     result = self.conn.read(database='votes', query=q)
    #     # print(f'get_data: result: {result}')
    #     cleaned_data = []
    #     for record in result:
    #         cleaned_data.append(record)
    #     return cleaned_data

    # def get_all_question_choices(self):
    #     q = """
    #     MATCH (c:Choice)-[r]->(q:Question) RETURN c.name as choice, q.name as question
    #     """
    #     result = self.conn.read(database='votes', query=q)
    #     # print(f'get_data: result: {result}')
    #     cleaned_data = []
    #     for record in result:
    #         cleaned_data.append(record)
    #     return cleaned_data

    def get_relationships(self):
        q = """
        MATCH (n)-[r]->(b) return n as source_node, b as target_node, type(r) as relationship
        """
        result = self.conn.read(database='votes', query=q)
        # print(f'get_relationships: result: {result}')

        # Return a list of tuples of (source_node, target_node, relationship)
        cleaned_data = []
        for record in result:
            # Use dict values(key) to retrieve record info
            # EXAMPLE RECORD:
            # <Record source_node=<Node id=0 labels=frozenset({'Choice'}) properties={'name': "Can't Recall"}> target_node=<Node id=31 labels=frozenset({'Question'}) properties={'name': 'Where did you first hear of an Axo-lo-tle?'}> relationships='OPTION_OF'>
            print(f'get_relationships: record: {record.value("source_node")}')
            # Use dot notation to retrieve node properties
            source_node_id = record.value("source_node").id
            target_node_id = record.value("target_node").id
            relationship_type = record.value("relationship")
            cleaned_data.append((source_node_id, target_node_id, relationship_type))
        return cleaned_data

    def get_nodes(self):
        q = """
        MATCH (n) return n
        """
        result = self.conn.read(database='votes', query=q)
        # print(f'get_data: result: {result}')
        cleaned_data = []
        for record in result:
            # This will add a node record to the list
            # Use .dot notation to retrieve node values
            # EXAMPLE RECORD:
            # <Node id=33 labels=frozenset({'Choice'}) properties={'name': 'Asia'}>
            cleaned_data.append(record['n'])
        return cleaned_data
