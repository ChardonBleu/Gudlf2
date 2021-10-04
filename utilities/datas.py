import json


def load_clubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def load_competitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def research_club_in_clubs_by_email(clubs, club_email):
    return [club for club in clubs if club['email'] == club_email][0]


def research_club_in_clubs_by_name(clubs, club_name):
    return [club for club in clubs if club['name'] == club_name][0]


def research_competition_in_competitions_by_name(competitions,
                                                 competition_name):
    return [competition for competition in competitions if competition[
            'name'] == competition_name][0]