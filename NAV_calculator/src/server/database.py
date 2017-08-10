import json
import os

from flask_sqlalchemy import SQLAlchemy


class database(object):
    """docstring for database"""

    def __init__(self, app):
        super(database, self).__init__()
        self.app = app

        DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

        self.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.db = SQLAlchemy(self.app)

        self.FUND_DETAILS = self.db.Table('FUND_DETAILS',
                                         self.db.Column('id', self.db.Integer, primary_key=True),
                                         self.db.MetaData(bind=None),
                                         self.db.Column('fund_name', self.db.String(1000)),
                                         self.db.Column('date', self.db.Integer),
                                         self.db.Column('NAV', self.db.Float),
                                            autoload=True, autoload_with=self.db.engine)


    def insert_data(self, data):

        try:
            assert type(data) == list

            if len(data) == 0:
                return "no data recieved"

            self.db.engine.execute(self.FUND_DETAILS.insert(), data)
            return "successful"

        except Exception as e:
            return str(e)
        pass

    def json_output(self, condition, sql_obj):

        output = []
        if condition == 'get_unique':

            for i in sql_obj:
                out_str = {
                    "fund_name" : i[0]
                }
                output.append(out_str)

        elif condition == 'get_start_end_date':

            for i in sql_obj:
                out_str = {
                    "time" : int(i[0]),
                    "NAV" : i[1]
                }
                output.append(out_str)

        return output

    def query_data(self, id=None, data=None):

        #change the id when inserting a new data
        if id is None or not id.isdigit() or not 1 <= int(id) <= 2:
            return '{"remark" : "%s" }' % "invalid id"

        id = int(id)

        #get unique funds
        if id == 1:
            try:
                return json.dumps({"remark": "successful", "data": self.json_output('get_unique',
                                self.db.engine.execute('select distinct fund_name from "FUND_DETAILS"'))})
                #postgresql convension :: as it converts all to lower case and thus will lead to not finding the table

            except Exception as e:
                return '{"remark" : "get_unique_funds :: %s"}' % str(e)

        #get_start_end_date
        elif id == 2:

            if type(data) is not list:
                return '{"remark" : "%s" }' % "data as a list expected"

            if len(data)==0:
                return '{"remark" : "%s" }' % "data list is empty"

            try:
                QUERY = 'select date, NAV from "FUND_DETAILS"'
                QUERY += ' where fund_name = "'+(' - ').join(i for i in data)+'"'

                return json.dumps({"remark": "successful", "data": self.json_output('get_start_end_date', self.db.engine.execute(QUERY))})

            except Exception as e:
                return '{"remark" : "%s" }' % str(e)
