""" Class to hold all the log data to write to database"""
import random
import datautility as du
import constants as const
from constants import NITE_LITE_DB, ASSIST_PROD_DB
from configuration import nite_lite_db, assist_prod_db

db_nite, db_assist, db = None, None, None


class SessionLogData:
    def __init__(self):
        self.prob_id = None
        self.orig_ans = None
        self.revised_ans = None
        self.user_cond_id = None
        self.user_cond_is_treated = False
        self.log_actions = []
        self.log_suggestions = []

    def set_prob_id(self, _id):
        self.prob_id = _id

    def set_user_cond_id(self, _id):
        self.user_cond_id = _id

    def set_user_cond_is_treated(self, val):
        self.user_cond_is_treated = val

    def set_orig_ans(self, ans):
        self.orig_ans = ans

    def set_revised_ans(self, ans):
        self.revised_ans = ans

    def add_action_log(self, action_name, timestamp):
        self.log_actions.append([action_name, timestamp])

    def add_suggestions(self, responses):
        self.log_suggestions.append(responses["ans_rec_1"])
        self.log_suggestions.append(responses["ans_rec_2"])
        self.log_suggestions.append(responses["ans_rec_3"])

    def wrap_session_data(self):
        session_data = {
            "prob_id": self.prob_id,
            "user_cond_id": self.user_cond_id,
            "actions": self.log_actions,
            "suggestions": self.log_suggestions,
            "original_answer": self.orig_ans,
            "revised_answer": self.revised_ans
        }

        return session_data


# ----------------------------------- Helper Functions-------------------------------- #


def connect_db(dbname):
    if dbname == NITE_LITE_DB:
        db_object = du.db_connect(nite_lite_db['db_name'], nite_lite_db['username'], nite_lite_db['password'],
                                  host=nite_lite_db['host'], port=nite_lite_db['port'])
    else:
        db_object = du.db_connect(assist_prod_db['db_name'], assist_prod_db['username'], assist_prod_db['password'],
                                  host=assist_prod_db['host'], port=assist_prod_db['port'])
    return db_object


def get_db(dbname):
    global db_nite, db_assist
    if dbname == NITE_LITE_DB:
        if db_nite is None:
            db_nite = connect_db(dbname)
        return db_nite
    elif dbname == ASSIST_PROD_DB:
        if db_assist is None:
            db_assist = connect_db(dbname)
        return db_assist


def get_by_id(table, _id, dbname):
    query = 'SELECT * FROM {} WHERE id = {};'.format(table, _id)
    row, col = du.db_query(get_db(dbname), query, return_column_names=True)

    if len(row) == 0:
        return None

    res = dict()
    for c in range(len(col)):
        res[col[c]] = row[0][c]

    return res


def get_first_by_column(table, column, value, dbname):
    if isinstance(value, (list,)) and len(value) > 0:
        v = '('
        v += '\'{}\''.format(value[0]) if isinstance(value[0], str) else str(value[0])
        for i in range(1, len(value)):
            v += ',' + '\'{}\''.format(value[i]) if isinstance(value[i], str) else str(value[i])
        value = v + ')'
    else:
        value = '\'{}\''.format(value) if isinstance(value, str) else str(value)

    query = 'SELECT * FROM {} WHERE {} = {};'.format(table, column, value)
    try:
        row, col = du.db_query(get_db(dbname), query, return_column_names=True)
    except ValueError:
        return None

    if len(row) == 0:
        return None

    res = dict()
    for c in range(len(col)):
        res[col[c]] = row[0][c]

    return res


def get_all_by_column(table, column, value, dbname):
    if isinstance(value, str):
        value = '\'{}\''.format(value)
    query = 'SELECT * FROM {} WHERE {} = {};'.format(table, column, value)
    row, col = du.db_query(get_db(dbname), query, return_column_names=True)

    if len(row) == 0:
        return None

    res = dict()
    for c in range(len(col)):
        res[col[c]] = []
        for r in range(len(row)):
            res[col[c]].append(row[r][c])

    return res


def get_problem_body(problem_id, dbname):
    res = get_all_by_column('public.problems', 'id', problem_id, dbname)
    if res is None:
        return None
    return res['body']


# ---------------------------------------Table Logging--------------------------------- #


def create_session_log(problem_id, user_condition_id):
    query = 'INSERT INTO nitelite.session_logs (problem_id, user_condition_id ) ' \
            'VALUES ({},{}) RETURNING id;'.format(problem_id, user_condition_id)

    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


def create_session_answers_log(session_id, answer_id):
    query = 'INSERT INTO nitelite.session_answers (session_id, answer_id) ' \
            'VALUES ({},{}) RETURNING id;'.format(session_id, answer_id)

    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


def create_actions_log(session_id, action_type_id, action_timestamp):
    query = 'INSERT INTO nitelite.actions (session_id, action_type_id, action_timestamp) ' \
            'VALUES ({},{},{}) RETURNING id;' \
        .format(session_id, action_type_id, 'timestamp with time zone \'{}\''.format(str(action_timestamp)))

    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


def get_action_type_by_name(action_type_name):
    action_type_id = get_first_by_column('nitelite.action_type', 'action_type_name', action_type_name, NITE_LITE_DB)
    if action_type_id is None:
        return get_by_id('nitelite.action_type', create_action_type(action_type_name), NITE_LITE_DB)
    return action_type_id


def create_action_type(action_type_name):
    query = 'INSERT INTO nitelite.action_type (action_type_name) ' \
            'VALUES (\'{}\') RETURNING id;'.format(action_type_name)

    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


def get_answers_log(answer_body, answer_type_id):
    answer = get_first_by_column('nitelite.answers', 'answer_body', answer_body, NITE_LITE_DB)
    if answer is None:
        return get_by_id('nitelite.answers', create_answers_log(answer_body, answer_type_id), NITE_LITE_DB)
    return answer


def create_answers_log(answer_body, answer_type_id):
    query = 'INSERT INTO nitelite.answers (answer_body, answer_type_id) ' \
            'VALUES (\'{}\',{}) RETURNING id;'.format(answer_body, answer_type_id)

    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


def get_answer_type_by_name(answer_type_name):
    answer_type_id = get_first_by_column('nitelite.answer_type', 'answer_type_name', answer_type_name, NITE_LITE_DB)
    if answer_type_id is None:
        return get_by_id('nitelite.answer_type', create_answer_type(answer_type_name), NITE_LITE_DB)
    return answer_type_id


def create_answer_type(answer_type_name):
    query = 'INSERT INTO nitelite.answer_type (answer_type_name) ' \
            'VALUES (\'{}\') RETURNING id;'.format(answer_type_name)
    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


# ---------------------------------Prob id mapping and User Conditions------------------------------------ #


def get_qc_pr_mapping_id(col_name, col_val):
    return get_first_by_column('nitelite.qc_pr_mapping', col_name, col_val, NITE_LITE_DB)


# TODO: untested
def get_qc_ids(ass_pr_id):
    val = get_qc_pr_mapping_id('assistments_pr_id', ass_pr_id)
    return val['id'], val['qc_pr_id']


def get_user_condition(ext_user_id):
    user_id = get_user(ext_user_id)["id"]
    user_cond = check_user_condition(user_id)

    if not user_cond:
        user_condition_id = create_user_condition(user_id)["id"]
        user_cond = get_by_id("nitelite.user_conditions", user_condition_id, NITE_LITE_DB)

    return user_cond


def check_user(ext_user_id):
    res = get_first_by_column("nitelite.users", "user_xref_id", ext_user_id, NITE_LITE_DB)
    return res


def create_user_id(ext_user_id):
    query = 'INSERT INTO nitelite.users (user_xref_id) ' \
            'VALUES (\'{}\') RETURNING id;'.format(ext_user_id)
    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


def get_user(ext_user_id):
    user = check_user(ext_user_id)
    if not user:
        return create_user_id(ext_user_id)
    return user


def check_user_condition(user_id):
    res = get_first_by_column("nitelite.user_conditions", "user_id", user_id, NITE_LITE_DB)
    return res


def create_user_condition(user_id):
    """
    False- Controlled(Probability: 1/6), True- Treated (Probability: 5/6).
    """
    condition_type = bool(random.randint(0, len(const.randomization_types)))
    if condition_type:
        randomize_id = random.randint(1, len(const.randomization_types))
        model_id = random.randint(1, len(const.model_types))

        query = 'INSERT INTO nitelite.user_conditions (user_id, user_condition_type_id, model_type_id, ' \
                'randomize_type_id) ' \
                'VALUES ({},{},{},{}) RETURNING id;'.format(user_id, 2, model_id, randomize_id)
    else:
        query = 'INSERT INTO nitelite.user_conditions (user_id, user_cond_type) ' \
                'VALUES ({},{}) RETURNING id;'.format(user_id, 1)

    return du.db_query(get_db(NITE_LITE_DB), query)[0][0]


# -------------------------------------------Master db write method------------------------------------------ #


def write_session_data_to_db(session_data):
    # write session logs --> session metadata
    session_id = create_session_log(session_data["prob_id"], session_data["user_cond_id"])

    # write action logs --> all action timestamps
    for action in session_data["actions"]:
        action_type = get_action_type_by_name(action[0])
        create_actions_log(session_id, action_type["id"], action[1])

    # write answer logs --> orig answer, revised answer, 3 suggestions
    for ans_type in ["original_answer", "revised_answer", "suggestions"]:
        if isinstance(session_data[ans_type], (list,)):
            for answer in session_data[ans_type]:
                ans_body = answer[0]
                ans_type_name = ans_type + "_" + answer[1]

                ans_type_id = get_answer_type_by_name(ans_type_name)["id"]
                # ans = get_answers_log(ans_body, ans_type_id)
                #
                # if ans is None:
                #     ans = create_answers_log(ans_body, ans_type_id)
                # create_session_answers_log(session_id, ans["id"])

                ans_id = create_answers_log(ans_body, ans_type_id)
                create_session_answers_log(session_id, ans_id)
        else:
            ans_type_id = get_answer_type_by_name(ans_type)["id"]
            # ans = get_answers_log(session_data[ans_type], ans_type_id)
            # create_session_answers_log(session_id, ans["id"])

            ans_id = create_answers_log(session_data[ans_type], ans_type_id)
            create_session_answers_log(session_id, ans_id)
