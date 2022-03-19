import random

from flask import Flask, render_template, request
import json
from generator import sentenceGenerate

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def getSentence():
    return render_template('index.html', sentence_generator=sentenceGenerate())


if __name__ == '__main__':
    app.run()
