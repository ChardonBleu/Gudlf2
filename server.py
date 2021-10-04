import json
from flask import Flask, render_template, request, redirect, flash, url_for, \
    session
import functools


def load_clubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def load_competitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def research_club_in_clubs_by_email(clubs, email):
    return [club for club in clubs if club['email'] == email][0]


def create_app(config):

    app = Flask(__name__)
    app.config.from_object("config")
    app.config["Testing"] = False

    # ########## Loading  datas from JSON files ################

    competitions = load_competitions()
    clubs = load_clubs()

    # ########### decorator @login_required ############

    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if session == {}:
                return redirect(url_for('login'))
            return view(**kwargs)
        return wrapped_view


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
                logged_club = research_club_in_clubs_by_email(clubs, email)
            except IndexError:
                error = 'Unknown club. Sorry.'
            else:
                error = None
                session.clear()
                session['name'] = logged_club['name']
                session['email'] = email
                print(session)
                return redirect(url_for('welcome'))

            flash(error)

        return render_template('login.html')

    @app.route('/welcome', methods=['GET'])
    @login_required
    def welcome():
        """It's necessary to be logged to acces this

        Returns:
            [type] -- welcome page with points club display
        """
        logged_club = research_club_in_clubs_by_email(clubs, session['email'])

        return render_template('welcome.html', logged_club=logged_club, clubs=clubs)

    @app.route('/showSummary', methods=['GET'])
    @login_required
    def showSummary():
        club = research_club_in_clubs_by_email(clubs, session['email'])

        return render_template('competitions.html',
                               club=club,
                               competitions=competitions)

    @app.route('/book/<competition>/<club>')
    @login_required
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',
                                   club=foundClub,
                                   competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('competitions.html',
                                   club=club,
                                   competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    @login_required
    def purchasePlaces():
        competition = [
            c for c in competitions if c['name'] == request.form['competition']
            ][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
        -placesRequired
        flash('Great-booking complete!')
        return render_template('competitions.html',
                               club=club,
                               competitions=competitions)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app
