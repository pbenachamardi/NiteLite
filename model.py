import constants as const

ans_rec_1 = "You can’t laugh at the same joke over and over. So why are you always crying about " \
            "the same problem?"
ans_rec_2 = "The frog consistently kept attempting to jump out of the boiling water, but was unable" \
            " to! The story is a lie"
ans_rec_3 = "When adversity knocks on your door, how do you respond? Are you a potato, an egg, or a " \
            "coffee bean? You can’t laugh at the same joke over and over. So why are you always crying " \
            "about the same problem?"


class NiteLiteModel(object):
    def __init__(self):
        self.name = "NiteLite"

        self.model = None
        self.randomize = None
        self.stud_ans = None

    def suggest_responses(self, stud_answer, model_id=1, rand_id=1):

        self.randomize = const.randomization_types.get(str(rand_id))
        self.model = const.model_types.get(str(model_id))
        self.stud_ans = stud_answer

        responses = {}

        if self.randomize is const.TWO_SIM_ONE_DIFF:
            responses = self.get_two_sim_one_diff()
        elif self.randomize is const.TEACHER_EXEMPLARS:
            responses = self.get_teacher_exemplars()
        elif self.randomize is const.STUDENT_ANSWERS:
            responses = self.get_stud_answers()
        elif self.randomize is const.MIXED_ANSWERS:
            responses = self.get_mixed_answers()

        return responses

    def get_two_sim_one_diff(self):
        # TODO: call relevant model
        responses = {
            "ans_rec_1": [ans_rec_1, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_2": [ans_rec_2, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_3": [ans_rec_3, const.ANS_TYPE_TEACHER_EXEMPLAR]
        }
        return responses

    def get_teacher_exemplars(self):
        # TODO: call relevant model
        responses = {
            "ans_rec_1": [ans_rec_1, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_2": [ans_rec_2, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_3": [ans_rec_3, const.ANS_TYPE_TEACHER_EXEMPLAR]
        }
        return responses

    def get_stud_answers(self):
        # TODO: call relevant model
        responses = {
            "ans_rec_1": [ans_rec_1, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_2": [ans_rec_2, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_3": [ans_rec_3, const.ANS_TYPE_TEACHER_EXEMPLAR]
        }
        return responses

    def get_mixed_answers(self):
        # TODO: call relevant model
        responses = {
            "ans_rec_1": [ans_rec_1, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_2": [ans_rec_2, const.ANS_TYPE_STUDENT_ANSWER],
            "ans_rec_3": [ans_rec_3, const.ANS_TYPE_TEACHER_EXEMPLAR]
        }
        return responses
