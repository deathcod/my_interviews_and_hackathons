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

        self.AFRICAN_CUP = self.db.Table('AFRICAN_CUP',
                                         self.db.Column('id', self.db.Integer, primary_key=True),
                                         self.db.MetaData(bind=None),
                                         self.db.Column('year', self.db.Integer),
                                         self.db.Column('logo', self.db.String(1000)),
                                         self.db.Column('host_country_id', self.db.Integer,
                                                        self.db.ForeignKey('COUNTRY.id')))

        self.COUNTRY = self.db.Table('COUNTRY',
                                     self.db.Column('id', self.db.Integer, primary_key=True),
                                     self.db.MetaData(bind=None),
                                     self.db.Column('flag', self.db.String(1000)),
                                     self.db.Column('name', self.db.String(1000)),
                                     self.db.Column('description', self.db.String(1000)),
                                     self.db.Column('geometry', self.db.String(1000000)))

        self.STADIUM = self.db.Table('STADIUM',
                                     self.db.Column('id', self.db.Integer, primary_key=True),
                                     self.db.MetaData(bind=None),
                                     self.db.Column('name', self.db.String(1000)),
                                     self.db.Column('capacity', self.db.String(100)),
                                     self.db.Column('description', self.db.String(1000)),
                                     self.db.Column('image', self.db.String(1000)),
                                     self.db.Column('city', self.db.String(1000)),
                                     self.db.Column('geometry', self.db.String(100)),
                                     autoload=True, autoload_with=self.db.engine)

        self.PLAYER = self.db.Table('PLAYER',
                                    self.db.Column('id', self.db.Integer, primary_key=True),
                                    self.db.MetaData(bind=None),
                                    self.db.Column('name', self.db.String(1000)),
                                    self.db.Column('description', self.db.String(1000)),
                                    self.db.Column('image', self.db.String(1000)),
                                    self.db.Column('geometry', self.db.String(100)),
                                    autoload=True, autoload_with=self.db.engine)

        self.RELATION_CUP_STADIUM = self.db.Table('RELATION_CUP_STADIUM',
                                                  self.db.Column('id', self.db.Integer, primary_key=True),
                                                  self.db.MetaData(bind=None),
                                                  self.db.Column('cup_id', self.db.Integer,
                                                                 self.db.ForeignKey('AFRICAN_CUP.id')),
                                                  self.db.Column('country_id', self.db.Integer,
                                                                 self.db.ForeignKey('COUNTRY.id')),
                                                  self.db.Column('stadium_id', self.db.Integer,
                                                                 self.db.ForeignKey('STADIUM.id')),
                                                  autoload=True, autoload_with=self.db.engine)

        self.RELATION_CUP_COUNTRY_PLAYER = self.db.Table('RELATION_CUP_COUNTRY_PLAYER',
                                                         self.db.Column('id', self.db.Integer, primary_key=True),
                                                         self.db.MetaData(bind=None),
                                                         self.db.Column('cup_id', self.db.Integer,
                                                                        self.db.ForeignKey('AFRICAN_CUP.id')),
                                                         self.db.Column('country_id', self.db.Integer,
                                                                        self.db.ForeignKey('COUNTRY.id')),
                                                         self.db.Column('player_id', self.db.Integer,
                                                                        self.db.ForeignKey('PLAYER.id')),
                                                         self.db.Column('special_event', self.db.String(100)),
                                                         autoload=True, autoload_with=self.db.engine)

        self.RELATION_CUP_COUNTRY = self.db.Table('RELATION_CUP_COUNTRY',
                                                  self.db.Column('id', self.db.Integer, primary_key=True),
                                                  self.db.MetaData(bind=None),
                                                  self.db.Column('cup_id', self.db.Integer,
                                                                 self.db.ForeignKey('AFRICAN_CUP.id')),
                                                  self.db.Column('country_id_1', self.db.Integer,
                                                                 self.db.ForeignKey('COUNTRY.id')),
                                                  self.db.Column('country_id_2', self.db.Integer,
                                                                 self.db.ForeignKey('COUNTRY.id')),
                                                  self.db.Column('score', self.db.String(100)),
                                                  autoload=True, autoload_with=self.db.engine)

    def insert_data(self, id, data):

        if not id.isdigit() or not 1 <= int(id) <= 7:
            return "invalid id"
        try:
            assert type(data) == list
            id = int(id)

            if len(data) == 0:
                return "no data recieved"

            if id == 1:
                """Input for AFRICAN_CUP"""
                self.db.engine.execute(self.AFRICAN_CUP.insert(), data)
                return "successful"

            elif id == 2:
                """Input for COUNTRY"""
                self.db.engine.execute(self.COUNTRY.insert(), data)
                return "successful"

            elif id == 3:
                """Input for STADIUM"""
                self.db.engine.execute(self.STADIUM.insert(), data)
                return "successful"

            elif id == 4:
                """Input for PLAYER"""
                self.db.engine.execute(self.PLAYER.insert(), data)
                return "successful"

            elif id == 5:
                """Input for RELATION_CUP_STADIUM"""
                self.db.engine.execute(self.RELATION_CUP_STADIUM.insert(), data)
                return "successful"

            elif id == 6:
                """Input for RELATION_CUP_COUNTRY_PLAYER"""
                self.db.engine.execute(self.RELATION_CUP_COUNTRY_PLAYER.insert(), data)
                return "successful"

            elif id == 7:
                """Input for RELATION_CUP_COUNTRY"""
                self.db.engine.execute(self.RELATION_CUP_COUNTRY.insert(), data)
                return "successful"

            else:
                return "invalid entry"

        except Exception as e:
            return str(e)
        pass

    def json_output(self, table, sql_obj):

        output = []
        if table == 'COUNTRY':

            for i in sql_obj:
                out_str = {
                    "id" : i[0],
                    "geometry" : i[1],
                    "flag" : i[2],
                    "name" : i[3],
                    "description" : i[4],
                    "year" : i[5],
                    "logo" : i[6],
                    "score" : i[7],
                    "position" : i[8]
                }
                output.append(out_str)

        elif table == 'STADIUM':

            for i in sql_obj:
                out_str = {
                    "id": i[0],
                    "name": i[1],
                    "capacity": i[2],
                    "description": i[3],
                    "image" : i[4],
                    "city" : i[5],
                    "geometry": i[6]
                }
                output.append(out_str)

        elif table == 'PLAYER':

            for i in sql_obj:
                out_str = {
                    "id": i[0],
                    "name": i[1],
                    "description": i[2],
                    "image" : i[3],
                    "geometry": i[4]
                }
                output.append(out_str)

        return output

    def query_data(self, id):

        #change the id when inserting a new data
        if not id.isdigit() or not 1 <= int(id) <= 3:
            return '{"remark" : "%s" }' % "invalid id"

        id = int(id)

        #country
        if id == 1:
            try:
                return json.dumps({"remark": "successful", "data": self.json_output('COUNTRY',
                                self.db.engine.execute('''    
                                            select "COUNTRY".id as id, "COUNTRY".geometry as geometry, "COUNTRY".flag as flag, "COUNTRY".name as name, "COUNTRY".description as description, "AFRICAN_CUP".year as year,"AFRICAN_CUP".logo as logo,z.score as score, z.position as position from  
                                            (select cup_id as cup_id, country_id_1 as country_id, score as score, (case when(id %% 2 = 0) then 1 else 3 end) as position from "RELATION_CUP_COUNTRY"  
                                            union 
                                            select cup_id as cup_id, country_id_2 as country_id,score as score, (case when(id %% 2 = 0) then 2 else 4 end) as position from "RELATION_CUP_COUNTRY"
                                            union
                                            select id as cup_id, host_country_id as country_id, '0' as score, '5' as position from "AFRICAN_CUP") as z  
                                            left join "COUNTRY" 
                                            on z.country_id="COUNTRY".id 
                                            left join "AFRICAN_CUP" 
                                            on z.cup_id="AFRICAN_CUP".id 
                                            '''))})
                #postgresql convension :: as it converts all to lower case and thus will lead to not finding the table
                #postgresql convension :: do not use single % use double %%

            except Exception as e:
                return '{"remark" : "DATABASE :: %s"}' % str(e)

        #stadium
        elif id == 2:
            try:
                return json.dumps({"remark": "successful", "data": self.json_output('STADIUM', self.db.engine.execute(
                    'select * from \"STADIUM\"'))})

            except Exception as e:
                return '{"remark" : "%s" }' % str(e)

        #player
        elif id == 3:
            try:
                return json.dumps({"remark": "successful", "data": self.json_output('PLAYER', self.db.engine.execute(
                    'select * from \"PLAYER\"'))})

            except Exception as e:
                return '{"remark" : "%s" }' % str(e)

    def update_data(self, id, data):

        #change the id when inserting a new data
        if not id.isdigit() or not 1 <= int(id) <= 3:
            return "invalid id"
        try:
            # assert type(data) == dict
            # assert "description" in data and type(data["description"]) == str
            # assert "id" in data and type(data["id"]) == int

            id = int(id)
            #country
            if id == 1:
                self.db.engine.execute('update "COUNTRY" set description=\'%s\' where id=%d' % (data['description'], data['id']))
                return "successful"

            #stadium
            elif id == 2:
                self.db.engine.execute('update "STADIUM" set description=\'%s\' where id=%d' % (data['description'], data['id']))
                return "successful"

            #player
            elif id == 3:
                self.db.engine.execute('update "PLAYER" set description=\'%s\' where id=%d' % (data['description'],  data['id']))
                return "successful"

            else:
                return "invalid id"

        except Exception as e:
            return str(e)
