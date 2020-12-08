from _datetime import datetime
from flask import request, render_template, jsonify, session

from werkzeug.utils import redirect

import database as db
import model
import configuration as conf
import constants as const

app = conf.get_app()
log = db.SessionLogData()
nite_lite = model.NiteLiteModel()


@app.route('/')
def start_app():

    # ************ Remove once problem id is fixed ************* #
    session["prob_body"] = "If club members want to choose a list of projects for the year based on their " \
                           "budget and time, Given the cost and time for each project and the revenue it " \
                           "earns , what is the best return of investment?"
    session["prob_id"] = "PRATEST - GroupAssist"
    session["prob_num"] = "Question 1"

    # ****************************************** #

    if "orig_answer_submitted" not in session:
        session['assistments'] = 1

        log.add_action_log(const.SESSION_START, datetime.now())
        print("session_start", datetime.now())

        '''
        p1= User Reference (uuid)
        p2= Class Reference (uuid)
        p3= Assignment Reference (uuid)
        p4: External problem id(iframe id)
        p5: Problem id in assistments table
        '''
        # p1 = User Reference (uuid)
        if "p1" in request.args.keys():
            ext_user_id = request.args['p1']
        else:
            ext_user_id = const.dummy_url_params["p1"]

        # p5: Problem id in assistments table
        if 'p5' in request.args.keys():
            ass_pr_id = request.args['p5']  # Iframe sent problem ID?
        else:
            ass_pr_id = const.dummy_url_params["p5"]

        # p4: External problem id
        if 'p4' in request.args.keys():
            pr_id = request.args['p4']
        else:
            pr_id = const.dummy_url_params["p4"]

        log.set_prob_id(pr_id)  # log correct prob id p4/p5?

        # qc_pr_mapping_id, pr_id = db.get_qc_ids(ass_pr_id)
        user_cond = db.get_user_condition(ext_user_id)
        log.set_user_cond_id(user_cond["id"])

        prob_body = session["prob_body"]  # dummy
        # prob_body = db.get_problem_body(ass_pr_id, conf.assist_prod_db['db_name'])

        session['qc_id'] = ass_pr_id
        session['ass_pr_id'] = ass_pr_id
        session["prob_body"] = prob_body
        session['user_condition_type'] = user_cond['user_condition_type_id']
        session['model_id'] = user_cond['model_type_id']
        session['randomize_id'] = user_cond['randomize_type_id']

    return render_template('nite_lite.html')


@app.route("/submit/", methods=['POST'])
@app.route("/submit", methods=['POST'])
def submit_answer():
    if request.method == "POST":
        is_user_condition_treated = session['user_condition_type']

        if "orig_answer_submitted" not in session:
            # Student submitting answer for the first time
            stud_ans = request.form["answer"]
            if not stud_ans:
                return

            session["stud_ans"] = stud_ans
            log.set_orig_ans(stud_ans)
            log.add_action_log(const.ORIG_ANS_SUBMIT, datetime.now())

            if is_user_condition_treated:
                # Treated condition. Show suggestions to student
                responses = nite_lite.suggest_responses(stud_ans) \
                    # , session["model_id"], session["randomize_id"])
                if responses:
                    session["ans_rec_1"] = responses["ans_rec_1"][0]
                    session["ans_rec_2"] = responses["ans_rec_2"][0]
                    session["ans_rec_3"] = responses["ans_rec_3"][0]
                    log.add_suggestions(responses)

                session["show_recs_div"] = True
                session["orig_answer_submitted"] = True
            else:
                # Controlled condition. No suggestions. Finish Session.
                session["orig_answer_submitted"] = True
                finish_session()

            return render_template('nite_lite.html')
        else:
            # Student submitting revised/unchanged answer after seeing suggestions.
            stud_ans = request.form["answer"]
            log.set_revised_ans(stud_ans)
            log.add_action_log(const.FINAL_SUBMIT, datetime.now())

            session["stud_ans"] = stud_ans
            session["show_recs_div"] = False
            finish_session()

            return redirect('/')


@app.route("/resubmit_or_edit/", methods=['POST'])
def resubmit_or_edit():
    if request.method == "POST":
        session["show_recs_div"] = False

        if request.form.get("resubmit"):
            log.add_action_log(const.ORIG_ANS_RESUBMIT, datetime.now())
            finish_session()

            return redirect('/')

        elif request.form.get("edit"):
            log.add_action_log(const.EDIT_BUTTON_CLICK, datetime.now())

            return render_template('nite_lite.html')


@app.route("/test", methods=['GET'])
def revise_answer_test():
    return render_template('nite_lite.html')


@app.route("/_cleanup")
def cleanup():
    session.clear()
    return jsonify([])


def finish_session():
    session["success"] = True
    log.add_action_log(const.SESSION_END, datetime.now())

    session_data = log.wrap_session_data()
    print(session_data)
    db.write_session_data_to_db(session_data)


if __name__ == '__main__':
    app.run()
