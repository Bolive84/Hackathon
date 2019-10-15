import pickle
import flask
import pandas as pd
import numpy as np
import datetime
app = flask.Flask(__name__)

pipe = pickle.load(open("pipe.pkl", "rb"))

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if flask.request.method == 'POST':
        inputs = flask.request.form
        # print(inputs['positive_affect'])
        date = str(inputs['published_date'])
        unix_ts = datetime.datetime.strptime(date, '%Y-%m-%d')
        published_date = int(unix_ts.timestamp())

        data = pd.DataFrame([{
            'description': inputs['description'],
            'duration': inputs['duration'],
            'languages': inputs['languages'],
            'published_date': published_date,
            'tags': inputs['tags'],
            'title': inputs['title']
        }])

        viral = pipe.predict(data)[0]

        if (viral == 1):
            prediction = 'will be'
        else:
            prediction = 'will not be'

        return flask.render_template("results.html", prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
