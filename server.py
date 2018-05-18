from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
from sqlalchemy.orm import sessionmaker
from schema_defsv3 import *
from graph import *
import uuid
import json

DATABASE={'user':'sqlite:///toolusage.db'}
app = Flask(__name__)
engines = []
class session_tool_duration:
    def __init__(self,duration,session_id,tool_id):
        self.duration = duration
        self.session_id = session_id
        self.tool_id = tool_id

TABLE_USER = users
TABLE_TOOLS = tooldata
TABLE_SESSIONS = sessiondata
TABLE_SESSION_UID = usersession
engine = create_engine(DATABASE['user'],echo=True)

Session = sessionmaker(bind=engine)
s = Session()
js={}
@app.route('/')
def home(uid=None,role=None):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        query = s.query(TABLE_TOOLS.toolname,TABLE_TOOLS.url,TABLE_TOOLS.toolid)
        temp = query.all()
        print temp
        temp_tup = []
        for tup in temp:
            tmp_dict = {}
            tmp_dict['name']=tup[0]
            tmp_dict['url']=tup[1]
            tmp_dict['id']=tup[2]
            temp_tup.append(tmp_dict)
        js['tools'] = temp_tup
        print "souradeep"
        #print js['tools']
        js['session_id'] = uid
        jsonify(js)
        print js
        if(str(role)!='ADMIN'):
            return render_template('home.html',js=js)
        else:
            return render_template('dashboard.html')

@app.route('/home/data',methods=['GET','POST'])
def update_session_time():
    YSession = sessionmaker(bind=engine)
    y = YSession()

    data = request.get_json()
    print data
    if (data['flag']==True):

        START_TIME = str(data['time'])
        session['start_time'] = START_TIME
        session_data = TABLE_SESSIONS(xy=data['inst'],sessionid=data['session_id'],toolid=data['tool_id'],starttime=START_TIME,endtime=None,duration=None)
        y.add(session_data)
    else:

        query = y.query(TABLE_SESSIONS).filter_by(toolid=data['tool_id'],sessionid=data['session_id'],xy=data['inst'])
        update_row = query.first()
        if update_row:
            update_row.endtime = str(data['time'])
            update_row.duration = (int(data['time'])-int(update_row.starttime))
    y.commit()
    return json.dumps({'status':'OK'})

@app.route('/dashboard/graphone',methods=['GET','POST'])
def graph_one_data():
    return graph1_data()

@app.route('/dashboard/graphtwo',methods=['GET','POST'])
def graph_two_data():
    return graph2_data()


from base64 import b64encode
from os import urandom


@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])


    query = s.query(TABLE_USER).filter(TABLE_USER.userid.in_([POST_USERNAME]), TABLE_USER.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        random_bytes = urandom(64)
        token = b64encode(random_bytes).decode('utf-8')
        session['uid'] = token
        session['duration'] = 0
        #query = s.query(TABLE_SESSION_UID).filter(TABLE_SESSION_UID.userid.in_([POST_USERNAME]), TABLE_SESSION_UID.sessionid.in_()) )

        session['logged_in'] = True
        #here I will get the Userid_Session id class name#
        userid_session = TABLE_SESSION_UID(userid=POST_USERNAME,sessionid= session['uid'])
        s.add(userid_session)
        s.commit()
        return home(session['uid'],result.role)
    else:
        flash('wrong password!')
        return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return home()


if __name__ == "__main__":

    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=4000)
