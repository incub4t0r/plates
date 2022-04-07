#!/usr/bin/env python3

# https://docs.python.org/3/library/sqlite3.html

from flask import Flask, render_template, request, redirect, session, send_from_directory, make_response, jsonify
import sqlite3
import math

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return redirect('/calculator', 303)

def calcPlates(weight):
    results = {}
    perSide = (weight-45)/2
    num45 = math.floor(perSide / 45)
    num25 = math.floor((perSide - (num45*45))/25)
    num10 = math.floor((perSide - (num45*45) - (num25*25))/10)
    num5 = math.floor((perSide - (num45*45) - (num25*25) - (num10*10))/5)
    num2_5 = math.floor(
        (perSide - (num45*45) - (num25*25) - (num10*10) - (num5*5))/2.5)
    results['45'] = num45
    results['25'] = num25
    results['10'] = num10
    results['5'] = num5
    results['2.5'] = num2_5
    totalWeight = (num45*45 + num25*25 + num10*10 + num5*5 + num2_5*2.5)*2 + 45
    return (results, totalWeight)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'GET':
        return render_template('calculator.html')
    elif request.method == 'POST':
        results = {}
        totalWeight = float(request.form.get("weight"))
        if totalWeight < 45.0:
            return render_template('calculator.html', error="Do the math yourself")
        else:
            results = calcPlates(totalWeight)
            return render_template('calculator.html', data=results[0], weight=results[1])

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
