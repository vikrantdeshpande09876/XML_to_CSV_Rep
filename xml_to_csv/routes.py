from flask import Flask, render_template, redirect, request, flash, session, g
from .forms import LoginForm
from . import XML2CSV
from .main import Main
import os
from json import dumps

def getglobal(key):
    return g.get(key)
XML2CSV.jinja_env.globals.update(GET_GLOBAL=getglobal,)

def setglobal(key,val):
    setattr(g,key,val)
    return ''
XML2CSV.jinja_env.globals.update(SET_GLOBAL=setglobal,)

@XML2CSV.context_processor
def utility_functions():
    def print_in_console(m1):
        print (m1)
    return dict(mdebug=print_in_console)


@XML2CSV.route('/')
def homepage_default():
    return redirect('/login')
    
@XML2CSV.route('/login',methods=['GET','POST'])
def login():
    if 'validated' in session:
        return redirect('/home')
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

@XML2CSV.route('/result')
def result():
    if 'validated' in session:
        if 'filename' in session and 'selected_ftype' in session and 'path' in session:
            main=Main()
            main.exec_main_functions(session['path'], session['selected_ftype'])
            df_tag_nesting=main.retrieve_dataframe(main.arr_tag_nesting)
            main.write_dataframe_to_csv(XML2CSV.config['UPLOAD_DIR'],session['filename'],df_tag_nesting,',')
            session.clear()
        else:
            flash("Could not find session variables! Please try to refresh the page.")
    else:
        flash('You must be signed in to view that page!')
        return redirect('/login')
    return render_template('Result_XML_Checkboxes_Bkp.html',dataframe=main.arr_tag_nesting, title="Result | XML2CSV")