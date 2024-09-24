from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/digest')
def digest():
    return render_template('digest.html')

if __name__ == '__main__':
    app.run(debug=True)