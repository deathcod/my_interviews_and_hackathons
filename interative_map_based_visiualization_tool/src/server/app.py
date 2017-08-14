import json

from flask import Flask, request, render_template, url_for

from database import database

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "../../templates")
STATIC_DIR = os.path.join(CURRENT_DIR, "../../static")

app = Flask(__name__, template_folder= TEMPLATES_DIR, static_folder=STATIC_DIR)
DB = database(app)


def db_insert(id, data):
    return '{"remark": "%s"}' % DB.insert_data(id, data)

def db_query(id):
    return DB.query_data(id)

def db_update(id, data):
    return '{"remark": "UPDATE:: %s"}' % DB.update_data(id, data)

@app.route('/query', methods=['POST'])
def query():
    try:
        if not request.data:
            return '{"remark":"json data expected"}'

        data = request.data
        data = json.loads(data)

        if 'main_id' not in data:
            return '{"remark":"main_id expected"}'
        main_id = data['main_id']

        if not main_id.isdigit():
            return '{"remark": "invalid main id"}'

        #insert
        if int(main_id) == 1:
            if 'id' not in data:
                return '{"remark":"id expected"}'
            id = data['id']

            if 'data' not in data:
                return '{"remark":"data expected"}'

            input_data = data['data']
            return db_insert(id, input_data)

        #query
        if int(main_id) == 2:

            if 'id' not in data:
                return '{"remark":"id expected"}'
            id = data['id']

            return db_query(id)

        # update
        if int(main_id) == 3:
            if 'id' not in data:
                return '{"remark":"id expected"}'
            id = data['id']

            if 'data' not in data:
                return '{"remark":"data expected"}'

            input_data = data['data']
            return db_update(id, input_data)

        else:
            return '{"remark": "invalid main id"}'
    except Exception as e:
        return '{"remark": "APP :: %s"}' % str(e)


@app.route('/')
def welcome_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
