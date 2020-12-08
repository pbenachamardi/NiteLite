from flask import Flask

nite_lite_db = dict()
nite_lite_db['alias'] = 'nite_lite_db'
nite_lite_db['db_name'] = 'postgres'
nite_lite_db['username'] = 'postgres'
nite_lite_db['password'] = 'wpiassistment'
nite_lite_db['host'] = 'problems.cys6auvzw1bb.us-east-1.rds.amazonaws.com'
nite_lite_db['port'] = '5432'

assist_prod_db = dict()
assist_prod_db['alias'] = 'assist_prod_db'
assist_prod_db['db_name'] = 'assistment_production'
assist_prod_db['username'] = 'postgres'
assist_prod_db['password'] = 'RuePierre0614'
assist_prod_db['host'] = 'dev.tng.cs.wpi.edu'
assist_prod_db['port'] = '5432'  # TODO: test connection on same port!

__app = None


def __create_app():
    global __app
    __app = Flask(__name__)
    __app.secret_key = 'bHfwUg3gj5dgkfs2Gyjn47fH8ifD94Ve'
    return __app


def get_app():
    global __app
    if __app is None:
        return __create_app()
    return __app
