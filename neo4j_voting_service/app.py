from operator import ge
from neo4j_voting_service.neo4j_repo import Neo4jRepository
from neo4j_voting_service.neo4j_utils import Neo4jConnection
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from typing import List, Tuple, Dict
import uuid
from pyvis import network as net
from pyvis import options as opts
from stvis import pv_static


# Questions list in sequential order
questions = [
    {
        'question' : 'Where did you first hear of an Axo-lo-tle?',
        'options' : ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Australia and Pacific', "Can't Recall"]
    },
        {
        'question' : "What's an Axo-lo-ltle's most interesting trait?",
        'options' : ["Can survive the vacuum of space", 'Can regnerate body parts', 'Can generate an electric shock', "No Idea"]
    },
        {
        'question' : 'What brings you to GraphConnect?',
        'options' : ['Interest in Learning', 'To connect with other graph enthusasists', 'Was forced to']
    },
]

# questions = [
#     {
#         'question' : 'Where did you first hear of an Axo-lo-tle?',
#         'options' : ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Australia and Pacific', "Can't Recall"]
#     }
# ]

# Check & Load existing answer state
# ANSWER_KEY = "answers"
def get_existing_answers()->dict[str:str]:
    """
    Get any existing answers from streamlit's session state
    
    Args:
        None
    
    Returns:
        dict: A dict[str:str] containing [question:selected_answer].
    """
    if "answers" not in st.session_state:
        answers = {}
    else:
        answers = st.session_state["answers"]
    return answers

def have_submitted_answers():
    if "submitted" not in st.session_state:
        return False
    return st.session_state["submitted"]

answers = get_existing_answers()
n4j = Neo4jRepository(st.secrets['neo4j_uri'], st.secrets['neo4j_user'], st.secrets['neo4j_password'])
# UNCOMMENT if wanting to autorefresh instead
# count = st_autorefresh(interval=2500, key="auto_refresh")

def submit_answers(uid: str, answers: dict[str:str]) -> bool:
    # n4j = Neo4jRepository(st.secrets['neo4j_uri'], st.secrets['neo4j_user'], st.secrets['neo4j_password'])
    success, message = n4j.submit_choices(uid, answers)
    if success == False:
        st.error(f"There was an error submitting your answers: {message}")
        return
    st.success(f"Your answers were submitted successfully")
    st.session_state["submitted"] = True

def select_answer(question: str, answer: str):
    answers[question] = answer
    st.session_state["answers"] = answers

def answers_for(question: str) -> List[str]:
    """
    Get the answers for a question

    Parameters:
    question (str): The question to get answers for

    Returns:
    List[str]: The answers for the question

    """
    for block in questions:
        if block['question'] == question:
            return block['options']
    raise Exception(f"Question not found in questions: {question}")

def next_question(list_of_questions: List[dict[str, str]], current_answers: dict[str:str]) -> str:
    """
    Present the next question in the list

    Parameters:
    list_of_questions (List[dict[str, str]]): List of questions to present
    current_answers (dict[str:str]): Dictionary of [questions:selected_answers]

    Returns:
    str: The question to be presented. None if there are no more questions. Throws an error if answer not apart of question options

    """
    # print(f'next_question: list_of_questions: {list_of_questions}')
    for _, option in enumerate(list_of_questions):
        # print(f'next_question: option: {option}')
        if option['question'] in current_answers:
            # print(f'next_question: question already answered')
            # We have an answer for this question already, check next
            continue
        # No answer yet for this question, present it
        # print(f'next_question: new question: {option["question"]}')
        return option['question']
    # No more questions!
    # print(f'next_question: no more questions')
    return None

def get_state(key):
    if key in st.session_state:
        return st.session_state[key]
    return None

uid = get_state('uuid')
if uid == None:
    uid = str(uuid.uuid4())[-5:]
    st.session_state['uuid'] =  uid

def intro():
    st.header('Introductory Poll')

def present_question(question: str, options: List[str]):
    st.header(question)
    for option in options:
        if st.button(option):
            select_answer(question, option)
            st.experimental_rerun()

def display_graph(network: net.Network, neo4j: Neo4jConnection):
    data = neo4j.get_data()
    print(f'display_graph: {data}')
    network.clear()
    for element in data:
        # Edge or node?
        network.add_node(element['name'])

def present_graph():
    end_screen = st.empty()
    with end_screen.container():
        n=net.Network(height='500px', width='500px',heading='')
        nodes = n4j.get_nodes()
        # print(f'nodes: {len(nodes)}')
        for _, record in enumerate(nodes):
            # Edge or node?
            label = list(record.labels)[0] # Should only have one label for the demonstrator
            # print(f'display element: {record}')
            idx = record.id
            if label == "User":
                if record['name'] == uid:
                    n.add_node(idx, label=record['name'], color='Green', labelHighlightBold=True)
                else:
                    n.add_node(idx, label=record['name'], color = 'DarkSeaGreen')
            elif label == "Question":
                n.add_node(idx, label=record['name'], color = "IndianRed")
            elif label == "Choice":
                n.add_node(idx, label=record['name'], color = "CornflowerBlue")

        edges = n4j.get_relationships()
        # print(f'edges: {edges}')
        for source_id, target_id, type in edges:
            # print(f'edges: {source_id} {target_id} {type}')
            n.add_edge(source_id, target_id, title=type)
        n.show_buttons(filter_=['physics'])
        pv_static(n)
    if st.button('Refresh'):
        print('refreshing')

def present_end():

    st.header('Thanks for answering!')
    description = f"Here's how the poll answers look like as a graph.  Your randomly generated user id is <b style='font-family:sans-serif; color:Green; font-size: 24px;'>  {uid}</b>"
    st.markdown(description, unsafe_allow_html=True)
    
    present_graph()

    more_info = f"""
    To explore this data more, use the <a href="https://neo4j.com/developer/neo4j-desktop/">Desktop app</a> or the <a href="https://neo4j.com/developer/neo4j-browser/">Neo4j Browser</a> from an <a href="https://neo4j.com/cloud/platform/aura-graph-database">AuraDB instance</a> with the following credentials: 
    <p style='font-family:sans-serif; font-size: 16px;'>
    uri: <b>{st.secrets['neo4j_uri']}</b>
    <br>user: <b>{st.secrets['neo4j_client_user']}</b>
    <br>pass: <b>{st.secrets['neo4j_client_password']}</b>
    </p>
    """
    st.markdown(more_info, unsafe_allow_html=True)

def main():
    next = next_question(questions, answers)
    if next is None:
        if have_submitted_answers() == False:
            submit_answers(uid, answers)
        present_end()
    else:
        next_options = answers_for(next)
        present_question(next, next_options)

main()