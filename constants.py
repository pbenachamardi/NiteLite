# Dummy url params
dummy_url_params = {
    "p4": 3005,
    "p5": 1804592,
    "p1": "1111"
}

# Answer Types
ANS_TYPE_STUDENT_ANSWER = 'student_answer'
ANS_TYPE_TEACHER_EXEMPLAR = 'teacher_exemplar'

# Action Types
SESSION_START = "session_start"
SESSION_END = "session_start"
ORIG_ANS_SUBMIT = "orig_ans_submit"
EDIT_BUTTON_CLICK = "edit_button_click"
ORIG_ANS_RESUBMIT = "orig_answer_resumit"
FINAL_SUBMIT = "final_submit"


# Randomization Types
STUDENT_ANSWERS = 'Student-Answers',
TEACHER_EXEMPLARS = 'Teacher-Exemplars',
TWO_SIM_ONE_DIFF = 'Two-Similar-One-Dissimilar',
MIXED_ANSWERS = 'Mixed-Answers-Exemplars'


# Model Types
SBERT_CANBERRA = 'Sentence-BERT-Canberra'


# Databases
NITE_LITE_DB = 'nite_lite_db'
ASSIST_PROD_DB = 'assist_prod_db'

# Maps
randomization_types = {
    '1': STUDENT_ANSWERS,
    '2': TEACHER_EXEMPLARS,
    '3': TWO_SIM_ONE_DIFF,
    '4': MIXED_ANSWERS
}

model_types = {
    '1': SBERT_CANBERRA
}
