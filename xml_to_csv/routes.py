from flask import Flask, render_template, redirect, request, flash, session, g
from .forms import LoginForm
from . import XML2CSV
from .main import Main
import os
import json

@XML2CSV.route('/')
def homepage_default():
    return redirect('/login')
    
@XML2CSV.route('/login',methods=['GET','POST'])
def login():
    if 'validated' in session:
        return render_template('Home.html',title='Home | XML2CSV')
    form=LoginForm()
    if form.validate_on_submit():
        if str.lower(form.username.data)=='v' and form.password.data=='v':
            session['validated']=True
            return redirect('/home')
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect('/login')
    return render_template('Login.html',form=form,title='Sign In | XML2CSV')

@XML2CSV.route('/home',methods=['GET','POST'])
def home():
    if 'validated' in session:
        return render_template('Home.html',title='Home | XML2CSV')
    else:
        flash('You must be signed in to view that page!')
        return redirect('/login')


@XML2CSV.route('/result',methods=['POST'])
def result():
    if 'validated' in session:
            for key in request.form.keys():
                data=key
            print("The raw data is= "+str(data))    #retrieves a JSON object with 0th element as our passed object from JS
            res_array=json.loads(data)['res_array']
            print("\n\nThe data_dictionary is= "+str(res_array))
            session.clear()
            main=Main()
            df=main.retrieve_dataframe(res_array)
            print("\n\n\nThe final dataframe is:\n")
            print(df)
    else:
        flash('You must be signed in to view that page!')
        return redirect('/login')
    return render_template('Result.html',title="Result | XML2CSV")