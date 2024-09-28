from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from espn_api.football import League
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

class Team(db.Model):
    name = db.Column(db.String, primary_key=True)
    owner = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    years_played = db.Column(db.Integer, nullable=False)
    championships = db.Column(db.Integer, nullable=False)
    mvps = db.Column(db.Integer, nullable=False)

class Matchup(db.Model):
    __tablename__ = 'matchups'
    
    matchup_id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    team1_score = db.Column(db.Float, default=0.0)
    team2_score = db.Column(db.Float, default=0.0)
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))

    team1 = db.relationship('Team', foreign_keys=[team1_id], backref='matchup_team1', lazy=True)
    team2 = db.relationship('Team', foreign_keys=[team2_id], backref='matchup_team2', lazy=True)
    winner = db.relationship('Team', foreign_keys=[winner_id], backref='matchup_winner', lazy=True)

class Schedule(db.Model):
    __tablename__ = 'schedule'
    
    schedule_id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)
    nfl_team1 = db.Column(db.String(80), nullable=False)
    nfl_team2 = db.Column(db.String(80), nullable=False)
 
    def __repr__(self):
        return f'Player {self.name}'

class ESPNFantasyFootballClient:
    def __init__(self):
        self.league_id = os.environ.get('ESPN_LEAGUE_ID')
        self.swid = os.environ.get('ESPN_SWID')
        self.espn_s2 = os.environ.get('ESPN_S2')
        self.year = datetime.now().year

        if not all([self.league_id, self.swid, self.espn_s2]):
            raise ValueError("Missing required ESPN API credentials")

        try:
            self.league = League(league_id=self.league_id, year=self.year, swid=self.swid, espn_s2=self.espn_s2)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to ESPN API: {str(e)}")

        self.teams = self.league.teams

    def get_teams(self):
        return [{"team_name": team.team_name} for team in self.teams]

    def get_standings(self):
        standings = []
        for team in self.teams:
            standings.append({
                "team_name": team.team_name,
                "wins": team.wins,
                "losses": team.losses,
                "points_for": team.points_for,
                "points_against": team.points_against
            })
        return standings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/digest')
def digest():
    return render_template('digest.html')

@app.route('/standings')
def standings():
    return render_template('standings.html')

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/api/teams', methods=['GET'])
def get_teams():
    client = ESPNFantasyFootballClient()
    teams = client.get_teams()
    return jsonify(teams)

@app.route('/api/standings', methods=['GET'])
def get_standings():
    client = ESPNFantasyFootballClient()
    standings = client.get_standings()
    return jsonify(standings)

if __name__ == '__main__':
    app.run(debug=True)