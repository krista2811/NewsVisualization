import uuid

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

import elastic
import json
import sys
import matplotlib.pyplot as plt

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
          
def get_plot(time, keywords):
    for (key, value) in keywords.items():
        plt.plot(time, value, label=key)
    size = len(time)
    print("a")
    sizes = [0, int(size/4), int(size/2), int(size*3/4), int(size-1)]
    print("b")
    ticks = [time[sizes[0]], time[sizes[1]], time[sizes[2]], time[sizes[3]], time[sizes[4]]]
    plt.xticks(ticks, [a.split("-")[0] for a in ticks])
    plt.legend(loc='upper left')
    fig = plt.figure()
    return fig

def show_plot(time, keywords):
    get_plot(time, keywords)
    plt.show()

def get_keyword_hist(titles):
    time = []
    keywords = {}
    for key in titles:
        keywords[key] = []

    for aggr in query.get_hist(titles):
        if aggr['doc_count'] == 0:
            continue
        time.append(aggr['key_as_string'])
        for (key, value) in aggr['5']['buckets'].items():
            keywords[key].append(value['doc_count'])    

    # plot(time, keywords)
    return {"time": time, "keywords": keywords}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hist', methods=['POST'])
def post():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str)
        args = parser.parse_args()
        keywords = args['query'].split(',')
        for i in range(len(keywords)):
            keywords[i] = keywords[i].strip(" ")
        data = get_keyword_hist(keywords)

        time = data['time']
        keywords = data['keywords']
        # for (key, value) in keywords.items():
        #     plt.plot(time, value, label=key)

        # size = len(time)
        # sizes = [0, int(size/4), int(size/2), int(size*3/4), int(size-1)]
        # ticks = [time[sizes[0]], time[sizes[1]], time[sizes[2]], time[sizes[3]], time[sizes[4]]]
        # plt.xticks(ticks, [a.split("-")[0] for a in ticks])
        # plt.legend(loc='upper left')
        # plt.savefig("fig.jpg", format='jpg')
        # plt.clf()

        # return render_template('plot.html', contents=keywords, plot="fig.jpg")
        return jsonify(data)
    except Exception as e:          
        return e

if __name__ == '__main__':
    app.run()