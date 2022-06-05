from operator import ge

# from async_timeout import Any
from neo4j_voting_service.neo4j_repo import Neo4jRepository
from neo4j_voting_service.neo4j_utils import Neo4jConnection
import streamlit as st
# from neo4j_voting_service import Neo4jRepository
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
        answers = {"":""}
    else:
        answers = st.session_state["answers"]
    return answers

answers = get_existing_answers()

def submit_answers(uid: str, answers: dict[str:str]) -> bool:
    n4j = Neo4jRepository(st.secrets['neo4j_uri'], st.secrets['neo4j_user'], st.secrets['neo4j_password'])
    success, message = n4j.submit_choices(uid, answers)
    if success == False:
        st.error(f"There was an error submitting your answers: {message}")
        return
    st.success(f"Your answers were submitted successfully")

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

def next_question(list_of_questions: List[dict[str, str | List[str]]], current_answers: dict[str:str]) -> str:
    """
    Present the next question in the list

    Parameters:
    list_of_questions (List[dict[str, str]]): List of questions to present
    current_answers (dict[str:str]): Dictionary of [questions:selected_answers]

    Returns:
    str: The question to be presented. None if there are no more questions. Throws an error if answer not apart of question options

    """
    for _, option in enumerate(list_of_questions):
        if option['question'] in current_answers:
            # We have an answer for this question already, check next
            continue
        # No answer yet for this question, present it
        return option['question']
    # No more questions!
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


def present_end():
    st.header('Thank you for your answers')
    # TODO: Show results
    g=net.Network(height='500px', width='500px',heading='')
    # g.set_edge_smooth('discrete')
    # g.show_buttons(filter_=['physics'])
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1,2)
    g.add_edge(2,3) 
    g.show_buttons(filter_=['physics'])
    pv_static(g)
    st.text(f'Your randomly generated id is {uid}')

def main():
    # st.header('Welcome to the Neo4j for Python Developers Workshop')
    next = next_question(questions, answers)
    if next is None:
        submit_answers(uid, answers)
        present_end()
    else:
        next_options = answers_for(next)
        present_question(next, next_options)
    # st.text(f'Your random UUID is {uid} ')

main()