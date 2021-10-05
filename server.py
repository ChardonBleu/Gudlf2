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

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))
    
    return app