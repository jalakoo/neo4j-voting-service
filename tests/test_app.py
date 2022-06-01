from neo4j_voting_service import app

test_questions = [
    {
        'question' : 'A',
        'options' : ['A1', 'A2', 'A3']
    },
        {
        'question' : "B",
        'options' : ["B1", "B2", "B3"]
    },
        {
        'question' : 'C',
        'options' : ['C1', 'C2', 'C3']
    },
]

def test_present_next_question():
    assert app.present_next_question(test_questions, ['A1']) == "B"
    assert app.present_next_question(test_questions, ['A1', 'B1']) == "C"
    assert app.present_next_question(test_questions, ['A1', 'B1', 'C1']) == None
