from src.data_extraction import scrapping
import pytest

def test__scrap_wiki_african_cup_of_nation():
    output = scrapping.scrap_wiki_african_cup_of_nation(DEPLOY=True)

    assert type(output) == dict
    assert "host_country" in output
    assert "country_1" in output
    assert "country_2" in output
    assert "score_1" in output
    assert "country_3" in output
    assert "country_4" in output
    assert "score_2" in output

    def check_score(key):
        for i in output[key]:
            assert len(i) != 0

        return len(key)

    def check_list(key):
        for i in key:
            assert len(i) >0


    def length_country(key):
        assert "flag" in output[key]
        assert "url" in output[key]
        assert "name" in output[key]

        check_list(output[key]["flag"])
        check_list(output[key]["url"])
        check_list(output[key]["name"])

        assert len(output[key]["flag"]) == len(output[key]["url"]) == len(output[key]["name"]) == 7

        return 7

    assert length_country("host_country") == length_country("country_1") == length_country("country_2") == check_score("score_1") == length_country("country_3") == length_country("country_4") == check_score("score_2") == 7

    pass


def test__african_cup_detail_per_year():

    stadium = {2006: 6, 2008: 4, 2010: 4, 2012: 4, 2013: 5, 2015: 4, 2017: 4}
    players = {2006: 2, 2008: 2, 2010: 2, 2012: 8, 2013: 3, 2015: 6, 2017: 2}

    for index,i in enumerate(stadium):

        output = scrapping.african_cup_detail_per_year(DEPLOY=True, year=i)

        assert "logo" in output
        assert "player" in output
        assert "stadium" in output

        assert "top-scorer" in output["player"]
        assert "best-player" in output["player"]

        assert len(output["player"]["top-scorer"]["player-name"]) == players[i] - 1
        assert len(output["player"]["top-scorer"]["country"]) == players[i] - 1
        assert len(output["player"]["best-player"]) == 1

        assert len(output["stadium"]["stadium_name"]) == stadium[i]
        assert len(output["stadium"]["capacity"]) == stadium[i]
        assert len(output["stadium"]["city"]) == stadium[i]


    # assert len(output["logo"]) == len(output["player"]["top-scorer"]) == len(output["player"]["best-player"]) == len(output["stadium"]) == 7
    #
    # for index, i in enumerate(stadium):
    #     assert len(output["stadium"]["stadium_name"]) == stadium[i]
    #     assert len(output["stadium"]["capacity"]) == stadium[i]
    #     assert len(output["stadium"]["city"]) == stadium[i]
    #
    # assert "top-scorer" in output["player"]
    # assert "best-player" in output["player"]
    #
    # for index, i in enumerate(players["top-scorer"]):
    #     assert len(output["player"]["top-scorer"]["country"]) == players[i]
    #     assert len(output["player"]["top-scorer"]["player-name"]) == players[i]
    #     assert len(output["player"]["top-scorer"]["goals-scored"]) == players[i]
    #
    # for index, i in enumerate(players["best-player"]):
    #     assert len(output["player"]["best-player"]["country"]) == players[i]
    #     assert len(output["player"]["best-player"]["player-name"]) == players[i]
    #
