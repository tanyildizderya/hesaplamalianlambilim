import random

from flask import Flask, render_template, request
import json
from generator import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def getSentence():
    if request.method == 'POST':
        if request.form.get('generator'):
            return render_template('index.html', sentence_generator=sentence_generator)


if __name__ == '__main__':
    app.run()
