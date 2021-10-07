from flask import Flask, render_template, request, redirect
from flask import flash, url_for, session

from utilities.datas import load_clubs, load_competitions
from utilities.datas import research_club_in_clubs_by_email
from utilities.datas import research_club_in_clubs_by_name
from utilities.datas import research_competition_in_competitions_by_name
from utilities.decorators import login_required


def create_app(config):

    app = Flask(__name__)
    app.config.from_object("config")
    app.config["Testing"] = False

    competitions = load_competitions()
    clubs = load_clubs()

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

    @app.route('/book/<competition_name>/<club_name>')
    @login_required
    def book(competition_name, club_name):
        found_club = research_club_in_clubs_by_name(clubs, club_name)
        found_competition = research_competition_in_competitions_by_name(
            competitions, competition_name)

        if found_club and found_competition:
            return render_template('booking.html',
                                   club=found_club,
                                   competition=found_competition)
        else:
            flash("Something went wrong-please try again")
            return render_template('competitions.html',
                                   club=found_club,
                                   competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    @login_required
    def purchasePlaces():
        competition = research_competition_in_competitions_by_name(
            competitions, request.form['competition'])
        club = research_club_in_clubs_by_name(clubs, request.form['club'])
        placesRequired = int(request.form['places'])
        if placesRequired > int(club['points']):
            flash('Not enough points available. Sorry.')
            return render_template('booking.html',
                                   club=club,
                                   competition=competition)
        elif placesRequired > int(competition['numberOfPlaces']):
            flash('Not enough places avalaible. Sorry')
            return render_template('booking.html',
                                   club=club,
                                   competition=competition)
        else:            
            competition['numberOfPlaces'] = str(int(
                competition['numberOfPlaces']) - placesRequired)
            club['points'] = str(int(club['points']) - placesRequired)
            flash('Great-booking complete!')
            return render_template('competitions.html',
                                club=club,
                                competitions=competitions,
                                competition=competition)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app
