import pickle
import flask
import pandas as pd
import numpy as np
import datetime
import random
import re
import marc
app = flask.Flask(__name__)

pipe = pickle.load(open("pipe.pkl", "rb"))

@app.route('/')
def home():
    mc = pickle.load(open("mc.pkl", "rb"))
    tags = pickle.load(open("tags.pkl", "rb"))
    length = (4, 8)
    n = 1
    for _ in range(n):
        l = random.randint(length[0], length[1])
        random_title = ' '.join(mc.next(n=l))
        random_title = re.sub(r'\s+([.,!?;])', r'\1', random_title)
    # size = range(len(tags))
    # print(tags)
    return flask.render_template('index.html', tags=tags, title=random_title)

@app.route('/result', methods=['POST'])
def result():
    if flask.request.method == 'POST':
        inputs = flask.request.form
        list_tags = inputs.getlist('tags')
        print(str(list_tags))
        # date = str(inputs['published_date'])
        # unix_ts = datetime.datetime.strptime(date, '%Y-%m-%d')
        # published_date = int(unix_ts.timestamp())

        data = pd.DataFrame([{
            'description': inputs['description'],
            'duration': inputs['duration'],
            'languages': inputs['languages'],
            'published_day': inputs['day'],
            'published_month': inputs['month'],
            'tags': str(list_tags),
            'title': inputs['title']
        }])

        viral = pipe.predict(data)[0]
        prob = np.round(pipe.predict_proba(data)[0][1] * 100, decimals=2)

        if (viral == 1):
            prediction = 'will be'
        else:
            prediction = 'will not be'

        return flask.render_template("results.html", prediction=prediction, prob=prob)

if __name__ == '__main__':
    app.run(debug=True)
