import json
from flask import Flask, render_template, request, redirect, flash, url_for, \
    session


def load_clubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def load_competitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def research_club_in_clubs(clubs, email):
    return [club for club in clubs if club['email'] == email][0]


def create_app(config):

    app = Flask(__name__)
    app.config.from_object("config")
    app.config["Testing"] = False

    # ########## Loading  datas from JSON files ################

    competitions = load_competitions()
    clubs = load_clubs()

    # ################# ROUTING ###################

    @app.route('/')
    @app.route('/index')
    def index():

        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            try:
                logged_club = research_club_in_clubs(clubs, email)
            except IndexError:
                error = 'Unknown club. Sorry.'
            else:
                error = None
                session.clear()
                session['name'] = logged_club['name']
                session['email'] = email
                print(session)
                return redirect(url_for('showSummary'))

            flash(error)

        return render_template('login.html')

    @app.route('/showSummary', methods=['GET'])
    def showSummary():
        club = research_club_in_clubs(clubs, session['email'])

        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',
                                   club=foundClub,
                                   competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [
            c for c in competitions if c['name'] == request.form['competition']
            ][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
        -placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app
