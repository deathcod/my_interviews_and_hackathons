import json
import logging

import scrapping


class arrange_data(object):
    """docstring for index"""

    def __init__(self, DEPLOY=False):
        super(arrange_data, self).__init__()

        self.DEPLOY = DEPLOY

        self.AFRICAN_CUP = []
        self.COUNTRY = []
        self.STADIUM = []
        self.PLAYER = []
        self.RELATION_CUP_STADIUM = []
        self.RELATION_CUP_COUNTRY = []
        self.RELATION_CUP_COUNTRY_PLAYER = []
        pass

    def __country(self, african_cup_detail):
        self.country_to_id_map = {}
        self.c_id = 0

        def country_row(country_index):

            for index, name in enumerate(african_cup_detail[country_index]['name']):
                if name.lower() not in self.country_to_id_map:
                    self.country_to_id_map[name.lower()] = self.c_id
                    row = {
                        'id': self.c_id,
                        'name': name,
                        'flag': african_cup_detail[country_index]['flag'][index],
                        'url': african_cup_detail[country_index]['url'][index]
                    }
                    self.COUNTRY.append(row)
                    self.c_id += 1
            pass

        for i in range(1, 5):
            country_row('country_' + str(i))

        country_row('host_country')

        # sequential scrapping of data, will implement multithreading later
        for i in self.COUNTRY:
            i['description'] = scrapping.get_wiki_page_description(DEPLOY=self.DEPLOY, title=i['name'])

        with open('geojson_data/c.json') as f:
            country_geojson = json.load(f)

        for i in country_geojson['features']:
            country_id = i['properties']['id']
            self.COUNTRY[country_id]["geometry"] = json.dumps(i['geometry'])

        # returning self for function chaining
        return self

    def __african_cup(self, african_cup_year_wise_detail, african_cup_detail):
        for index in range(len(self.year)):
            african_cup_row = {
                'id': index,
                'year': self.year[index],
                'logo': african_cup_year_wise_detail[index]['logo'][0],
                'host_country_id': self.country_to_id_map[african_cup_detail['host_country']['name'][index].lower()]
            }
            self.AFRICAN_CUP.append(african_cup_row)

        # returning self for function chaining
        return self

    def __relation_cup_country(self, african_cup_detail):
        for index in range(len(self.year)):
            row_cup_country1 = {
                'id': 2 * index,
                'cup_id': index,
                'country_id_1': self.country_to_id_map[african_cup_detail['country_1']['name'][index].lower()],
                'country_id_2': self.country_to_id_map[african_cup_detail['country_2']['name'][index].lower()],
                'score': ', '.join(african_cup_detail['score_1'][index])
            }
            self.RELATION_CUP_COUNTRY.append(row_cup_country1)
            row_cup_country2 = {
                'id': 2 * index + 1,
                'cup_id': index,
                'country_id_1': self.country_to_id_map[african_cup_detail['country_3']['name'][index].lower()],
                'country_id_2': self.country_to_id_map[african_cup_detail['country_4']['name'][index].lower()],
                'score': ', '.join(african_cup_detail['score_2'][index])
            }
            self.RELATION_CUP_COUNTRY.append(row_cup_country2)

        # returning self for function chaining
        return self

    def __stadium(self, african_cup_year_wise_detail):
        s_id = 0
        self.stadium_to_id_map = {}
        for i in african_cup_year_wise_detail:
            for index, name in enumerate(i['stadium']['stadium_name']):
                if name[1].lower() not in self.stadium_to_id_map:
                    self.stadium_to_id_map[name[1].lower()] = s_id
                    row_stadium = {
                        'id': s_id,
                        'name': name[1],
                        'capacity': i['stadium']['capacity'][index],
                        'city': i['stadium']['city'][index][1],
                    }
                    self.STADIUM.append(row_stadium)
                    s_id += 1

        # sequential scrapping of data, will implement multithreading later
        for i in self.STADIUM:
            i['description'] = scrapping.get_wiki_page_description(DEPLOY=self.DEPLOY, title=i['name'])
            i['image'] = scrapping.get_pic_url(DEPLOY=self.DEPLOY, query_word=i['name'])
            pass

        with open('geojson_data/s.json') as f:
            stadium_geojson = json.load(f)

        for i in stadium_geojson['features']:
            stadium_id = i['properties']['id']
            self.STADIUM[stadium_id]["geometry"] = json.dumps(i['geometry'])
        return self

    def __relation_cup_stadium(self, african_cup_detail, african_cup_year_wise_detail):
        rcts_id = 0
        for index, year_data in enumerate(african_cup_year_wise_detail):
            for i in year_data['stadium']['stadium_name']:
                stadium_name = i[1]
                row_cup_to_stadium = {
                    'id': rcts_id,
                    'cup_id': index,
                    'country_id': self.country_to_id_map[african_cup_detail['host_country']['name'][index].lower()],
                    'stadium_id': self.stadium_to_id_map[stadium_name.lower()]
                }
                self.RELATION_CUP_STADIUM.append(row_cup_to_stadium)
                rcts_id += 1

        return self

    def __player(self, african_cup_year_wise_detail):
        self.player_to_id_map = {}
        p_id = 0
        for year_data in african_cup_year_wise_detail:
            player = year_data['player']['top-scorer']['player-name']
            for index, player_name in enumerate(player):
                if player_name.lower() not in self.player_to_id_map and year_data['player']['top-scorer']['country'][
                    index].lower() in self.country_to_id_map:
                    self.player_to_id_map[player_name.lower()] = p_id
                    row_player = {
                        'id': p_id,
                        'name': player_name,
                    }
                    self.PLAYER.append(row_player)
                    p_id += 1
                    pass
                pass

            player_name = year_data['player']['best-player']['player-name'][0]
            if player_name.lower() not in self.player_to_id_map and year_data['player']['best-player']['country'][
                0].lower() in self.country_to_id_map:
                self.player_to_id_map[player_name.lower()] = p_id
                row_player = {
                    'id': p_id,
                    'name': player_name,
                }
                self.PLAYER.append(row_player)
                p_id += 1

        # sequential scrapping of data, will implement multithreading later
        for i in self.PLAYER:
            i['description'] = scrapping.get_wiki_page_description(DEPLOY=self.DEPLOY, title=i['name'])
            i['image'] = scrapping.get_pic_url(DEPLOY=self.DEPLOY, query_word=i['name'])
            pass

        with open('geojson_data/p.json') as f:
            player_geojson = json.load(f)

        for i in player_geojson['features']:
            player_id = i['properties']['id']
            self.PLAYER[player_id]["geometry"] = json.dumps(i['geometry'])

        return self

    def __relation_cup_country_player(self, african_cup_year_wise_detail):

        rccp_id = 0
        logging.info("Starting to arrange RELATION_CUP_COUNTRY_PLAYER")
        for index_year, year_data in enumerate(african_cup_year_wise_detail):
            player = year_data['player']['top-scorer']
            for index, i in enumerate(player['player-name']):
                if i.lower() in self.player_to_id_map:
                    row_cup_country_player = {
                        'id': rccp_id,
                        'cup_id': index_year,
                        'country_id': self.country_to_id_map[player['country'][index].lower()],
                        'player_id': self.player_to_id_map[i.lower()],
                        'special_event': player['goals-scored']
                    }
                    logging.debug('RELATION_CUP_COUNTRY_PLAYER:', row_cup_country_player)

                    self.RELATION_CUP_COUNTRY_PLAYER.append(row_cup_country_player)
                    rccp_id += 1

            if year_data['player']['best-player']['player-name'][0].lower() in self.player_to_id_map:
                row_cup_country_player = {
                    'id': rccp_id,
                    'cup_id': index_year,
                    'country_id': self.country_to_id_map[year_data['player']['best-player']['country'][0].lower()],
                    'player_id': self.player_to_id_map[year_data['player']['best-player']['player-name'][0].lower()],
                    'special_event': 'best-player'
                }
                self.RELATION_CUP_COUNTRY_PLAYER.append(row_cup_country_player)
                rccp_id += 1

        return self

    def start(self):
        african_cup_detail = scrapping.scrap_wiki_african_cup_of_nation(DEPLOY= self.DEPLOY)

        self.__country(african_cup_detail)

        self.year = [2006, 2008, 2010, 2012, 2013, 2015, 2017]
        african_cup_year_wise_detail = []

        # sequential scrapping of data, will implement multithreading later
        for i in self.year:
            african_cup_year_wise_detail.append(scrapping.african_cup_detail_per_year(DEPLOY=self.DEPLOY, year=i))

        self.__african_cup(african_cup_year_wise_detail, african_cup_detail)
        self.__relation_cup_country(african_cup_detail)
        self.__stadium(african_cup_year_wise_detail)
        self.__relation_cup_stadium(african_cup_detail, african_cup_year_wise_detail)
        self.__player(african_cup_year_wise_detail)
        self.__relation_cup_country_player(african_cup_year_wise_detail)

        #returning self for function chaining
        return self


if __name__ == '__main__':
    # x = arrange_data(DEPLOY=False).start()
    # scrapping.pretty_print_json(x.stadium_to_id_map)
    # print len(x.stadium_to_id_map)
    # scrapping.pretty_print_json(x.STADIUM)
    x = arrange_data(DEPLOY=False).start()
    # scrapping.pretty_print_json(x.COUNTRY)
    scrapping.pretty_print_json(x.AFRICAN_CUP)
    # print json.dumps(x.PLAYER)
    # print json.dumps(x.STADIUM)
    # print json.dumps(x.RELATION_CUP_STADIUM)
    # print json.dumps(x.RELATION_CUP_COUNTRY)
    # print json.dumps(x.RELATION_CUP_COUNTRY_PLAYER)
