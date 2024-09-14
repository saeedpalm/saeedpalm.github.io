from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/digest')
def digest():
    return render_template('digest.html')

@app.route('/standings')
def standings():
    return render_template('standings.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/players')
def players():
    return render_template('players.html')

if __name__ == '__main__':
    app.run(debug=True)