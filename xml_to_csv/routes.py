from flask import Flask, render_template, redirect, request, flash, session, render_template_string, url_for
from .forms import LoginForm
from . import XML2CSV
from .main import Main
from re import sub
import os,json


@XML2CSV.route('/')
def homepage_default():
    return redirect(url_for('login'))


@XML2CSV.route('/login',methods=['GET','POST'])
def login():
    if 'validated' in session:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        main=Main()
        fname=main.validate_user_creds(form.username.data,form.password.data,os.path.join(XML2CSV.config['STATIC_DIR'],'Login_creds.xlsx'))
        if fname:
            session['validated']=True
            session['username']=form.username.data
            session['fname']=fname
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect(url_for('login'))
    return render_template('Login.html',header='Sign In',form=form,title='Sign In | XML Parser')


@XML2CSV.route('/home',methods=['GET','POST'])
def home():
    if 'validated' in session:
        if request.method=='POST' and request.files:
            if str.lower('.'+request.form['ftype']) in request.files['filename'].filename:
                selected_file=request.files['filename']
                filename=selected_file.filename
                filesep=request.form['filesep']
                selected_ftype=request.form['ftype']
                path=os.path.join(XML2CSV.config['UPLOAD_DIR'],filename)
                try:
                    selected_file.save(path)
                    session['path']=path
                    session['selected_ftype']=selected_ftype
                    session['filename']=filename
                    session['filesep']=filesep
                    flash(filename+" saved at: "+str(path))
                except Exception as e:
                    flash("File couldn't be saved! \n"+e)
                return redirect(url_for('displayTags'))
            else:
                flash('Check the file format!')
                return redirect(url_for('login'))
        return render_template('Home.html',title='Home | XML Parser',header='Home | XML Parser')
    else:
        flash('Sign in to view that page!')
        return redirect(url_for('login'))



@XML2CSV.route('/home/displayTags',methods=['GET','POST'])
def displayTags():
    if 'validated' in session:
        if 'filename' in session and 'selected_ftype' in session and 'path' in session and 'filesep' in session and 'fname' in session:
            main=Main()
            overallstring=main.exec_main_functions(session['path'], session['selected_ftype'])
            overallstring='''
            {%extends "base.html"%}{%block content%}
            <div style="text-align:center;">
            <h1 id="myheader">Tags in <span style="color:green;">'''+session['filename']+'''</span> | XML Parser</h1>
            </div>
            {%assets "javascript_result"%}<script src="{{ ASSET_URL }}"></script>{%endassets%}
            <div id="subroot" class="container" style="max-width:94%;">
                <div id="root" class="container" style="max-width:90%; overflow:scroll;">'''+overallstring+'''
                </div>
                <label><b>Enter the Primary Parent Tag:   </b><input type="text" name="primary_parent_tag" id="primary_parent_tag"></label>
                <br>
                <br>
                <label><b>Enter the Primary Child Tag:   </b><input type="text" name="primary_child_tag" id="primary_child_tag"></label>
                <br>
                <br>
                <label><b>Enter the Primary Key Tag:   </b><input type="text" name="primary_key_tag" id="primary_key_tag"></label>
                <br>
                <br>
                <div style="text-align:center;">
                    <button class="mybtn" type="submit" id="generateConfigFile">Generate Config File</button>
                </div>
            </div>
            {%endblock%}'''
        else:
            print("Something went wrong. Try to parse the file again.")
            flash("Something went wrong. Try to parse the file again.")
            return redirect(url_for('home'))
    else:
        flash('Sign in to view that page!')
        return redirect(url_for('login'))
    return render_template_string(overallstring, title="TagNames | XML Parser")



@XML2CSV.route('/home/result',methods=['GET','POST'])
def home_result():
    if 'validated' in session:
        if 'filename' in session and 'selected_ftype' in session and 'path' in session and 'filesep' in session and 'fname' in session:
            for key in request.form.keys():
                    data=key
            #print("The raw data is= "+str(data))    #retrieves a JSON object with 0th element as our passed object from JS
            res_array=json.loads(data)['res_array']
            try:
                main=Main()
                template_path=os.path.join(XML2CSV.config['UPLOAD_DIR'],'Config_Template.csv')
                template_df=main.retrieve_template_dataframe(template_path)
                df=main.retrieve_final_dataframe(template_df,res_array)
                main.write_dataframe_to_excel(sub(session['filename'],'',session['path']),session['filename'],df)
                session['session_msg']='Your config file was created successfully '+session['fname']+'!'
                flash("Your dataframe was written successfully into the config.xlsx File!")
            except Exception as e:
                print("Could not write into config-excel File! Error is: "+str(e))
                flash("Could not write into config-excel File! Error is: "+str(e))
                return redirect(url_for('login'))
        else:
            print("Couldn't navigate to that page: Try selecting a file to parse again")
            flash("Couldn't navigate to that page: Try selecting a file to parse again")
            return redirect(url_for('login'))
    else:
        flash('Sign in to view that page!')
        return redirect(url_for('login'))
    return render_template('Result.html', title="Result | XML Parser")




@XML2CSV.route('/result',methods=['GET','POST'])
def result():
    if 'validated' in session:
        if 'session_msg' in session:
            session_msg=session['session_msg']
            fname=session['fname']
        else:
            flash('Parse a file to view the results!')
            return redirect(url_for('home'))
        if request.method=='POST':
            session.clear()
            session['validated']=True
            session['fname']=fname
            flash('Welcome back '+fname+'! Ready to parse another file?')
            return redirect(url_for('home'))
    else:
        flash('Sign in to view that page!')
        return redirect(url_for('login'))
    return render_template('Result.html', title="Result | XML Parser", header='Result | XML Parser',session_msg=session_msg)