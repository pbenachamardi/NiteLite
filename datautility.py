import psycopg2 as pg
import sys
import hashlib
import uuid


def db_connect(db_name, user, password='', host='127.0.0.1', port='5432'):
    return pg.connect(dbname=db_name, user=user, password=password, host=host, port=port)


def db_query(db_object, query, arguments=None, return_column_names=False):
    assert type(arguments) is dict or arguments is None

    if arguments is not None:
        for k in arguments:
            query = query.replace(str(k), arguments[k])

    cur = db_object.cursor()
    try:
        cur.execute(query)
        db_object.commit()
    except Exception:
        import traceback
        print('\033[91m')
        traceback.print_exc(file=sys.stdout)
        print(query + '\033[0m')

    try:
        if return_column_names:
            db_object.commit()
            return cur.fetchall(), [desc[0] for desc in cur.description]
        else:
            return cur.fetchall()
    except Exception:
        try:
            db_object.commit()
            return []
        except Exception:
            return None


def get_salted(password):
    salt = uuid.uuid4().hex
    enc = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return enc, salt


def compare_salted(password, encoded_password, salt):
    enc = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return enc == encoded_password
