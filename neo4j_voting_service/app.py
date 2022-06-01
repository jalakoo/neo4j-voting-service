from operator import ge
import streamlit as st
# from neo4j_voting_service import Neo4jRepository
from typing import List, Tuple, Dict
# import uuid

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

# Check & Load existing answer state
# ANSWER_KEY = "answers"
def get_existing_answers() -> List[str]:
    if "answers" not in st.session_state:
        answers = []
    else:
        answers = st.session_state["answers"]
    return answers

answers = get_existing_answers()

def submit_answers(answers: List[str]) -> bool:
    raise Exception('not yet implemented')

def select_answer(answer: str):
    answers.append(answer)
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

def next_question(list_of_questions: List[Dict[str, str]], current_answers: List[str]) -> str:
    """
    Present the next question in the list

    Parameters:
    list_of_questions (List[Dict[str, str]]): List of questions to present
    current_answers (List[str]): List of selected answers to questions

    Returns:
    str: The question to be presented. None if there are no more questions. Throws an error if answer not apart of question options

    """
    # Find last answer that matches the questions list
    if len(current_answers) == 0:
        # No answers yet
        return questions[0]['question']
    _answer = current_answers[-1]
    for index, option in enumerate(list_of_questions):
        if _answer in option['options']:
            if index >= len(list_of_questions) - 1:
                # We're on the last question
                return None
            else:
                # Get the question from the next question dict
                next_question_dict = list_of_questions[index + 1]
                return next_question_dict['question']
    raise Exception(f"Answer in answers not apart of question options. \nquestions: {list_of_questions}, \nanswers: {current_answers}")


# Don't need this for simplicity. Everyone will write to this db using this app's auth
# Assign a random uuid for a user when they start the app
# def update_only_blank_state(key, value):
#         """
#         Updates session state key-value. Returns value saved
#         or new value if written.
#         """
#         # Key does not yet exist
#         if key in st.session_state:
#             return st.session_state[key]
        
#         # Insert new key
#         st.session_state[key] = value
#         return value

# uid = update_only_blank_state('uuid', uuid.uuid1())

def intro():
    st.header('Introductory Poll')

def present_question(question: str, options: List[str]):
    st.header(question)
    for option in options:
        if st.button(option):
            select_answer(option)
            st.experimental_rerun()


def present_end():
    st.header('Thank you for your answers')
    # TODO: Show results

def main():
    # st.header('Welcome to the Neo4j for Python Developers Workshop')

    next = next_question(questions, answers)
    if next is None:
        submit_answers(answers)
        present_end()
    else:
        next_options = answers_for(next)
        present_question(next, next_options)
    # st.text(f'Your random UUID is {uid} ')

main()