#驗證碼  3日  google驗證
#權限
#export excel
#單量

from __future__ import print_function

from flask_qrcode import QRcode
import re

import pandas as pd
import gspread

from oauth2client.service_account import ServiceAccountCredentials
import uuid

from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

from flask import Flask, flash, redirect, render_template, request, session, abort,make_response, Response,url_for
app=Flask(__name__)
qrcode = QRcode(app)
app.config["SECRET_KEY"] = uuid.uuid4()
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 3
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SESSION_TYPE'] = 'sqlalchemy'
Session(app)
captcha = FlaskSessionCaptcha(app)

class DataStore():

    pp=None
    yy=None
    zza=None
    rr=None
    
data = DataStore()


@app.route('/')
def home():
    if not session.get('logged_in'):
        a=7
        return render_template('login.html',a=a)
    else:
        return render_template("home.html")

@app.route('/login', methods=['POST','GET'])
def do_admin_login():

    if data.zza ==2:
        session['counter'] =3
        data.zza-=1
    if 'counter' not in session:
        session['counter'] = 3
        data.zza=3
    if session.get('counter')>0:
        if request.form['password'] == 'e123' and request.form['username'] == 'admin' and captcha.validate():
            session['logged_in'] = True
            return render_template("home.html")
        elif request.form['password'] == 'e123' and request.form['username'] == 'agent' and captcha.validate():
            session['logged_in'] = True
            return render_template("homeagent.html")
        else:
            flash('wrong password!')
            session['counter'] = session.get('counter') - 1
            num=session['counter'] 
            num1='你還有'+str(num)+'次機會嘗試！'
            return render_template('login.html',num1=num1)
    else:
        # session.pop('counter', None)
        return render_template('loginfail.html')
      

@app.route("/logout", methods=['POST','GET'])
def logout():
        session['logged_in'] = False
        return redirect('/')

@app.route("/agentrecord", methods=['POST','GET'])
def agentrecord():
        return render_template('agentrecord.html')
@app.route("/clientrecord", methods=['POST','GET'])
def clientrecord():
        return render_template('clientrecord.html')
@app.route("/register", methods=['POST','GET'])
def register():
        return render_template('register.html')
@app.route("/clientregister", methods=['POST','GET'])
def clientregister():
        return render_template('clientregister.html')
@app.route("/register1", methods=['POST','GET'])
def register1():
        return render_template('register1.html')
@app.route("/clientregister1", methods=['POST','GET'])
def clientregister1():
        return render_template('clientregister1.html')
@app.route("/homeagent", methods=['POST','GET'])
def homeagent():
        return render_template('homeagent.html')


@app.route("/reset", methods=['POST','GET'])
def reset():
    if captcha.validate():
        data.zza=2
        session['counter']=0
        return redirect('/')
    else:
        return render_template('loginfail.html')
@app.route("/rebackhome", methods=['POST','GET'])
def rebackhome():
        return redirect('/')

@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")


@app.route("/getvip", methods=['POST','GET'])
def getvip():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    df=data.pp
    resp = make_response(df.to_csv().encode('utf-8-sig'))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    #resp.headers["Content-Type"] = "utf-8-sig"
    return resp

@app.route("/getcolleague", methods=['POST','GET'])
def getcolleague():
    df=data.yy
    resp = make_response(df.to_csv().encode('utf-8-sig'))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"

    return resp

@app.route("/getlocation", methods=['POST','GET'])
def getlocation():
    df=data.rr
    resp = make_response(df.to_csv().encode('utf-8-sig'))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"

    return resp

@app.route('/result',methods = ['POST'])
def result():
    prediction=''
    if request.method == 'POST':
        
        to_predict_list = request.form.to_dict()
     
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('./eclast.json', scope)
        client = gspread.authorize(creds)

        penny = client.open("Cogautoupdate").worksheet('cc')

        df=penny.get_all_records()


        lpp=[]
        for zz in range(len(df)):
            llz=[]
            for z,i in df[zz].items():
                llz.append(str(i))
            lpp.append(llz)
        dic={}
        for i in range(len(df)):
            dic.update({str(i):lpp[i]})
        df=pd.DataFrame.from_dict(dic, orient='index',columns=df[0].keys())
        df=df.drop(columns='世紀21經紀客人登記RomanTest_Id')
        df=df.loc[df.經紀姓名.str.contains(to_predict_list['z'],case=False)]
        return render_template("result.html",tables=[df.to_html(classes='data')])

@app.route('/pass1',methods = ['POST'])
def pass1():
    prediction=''
    if request.method == 'POST':
        
        to_predict_list = request.form.to_dict()
     
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('./eclast.json', scope)
        client = gspread.authorize(creds)

        penny = client.open("Cogautoupdate").worksheet('cc')

        df=penny.get_all_records()


        lpp=[]
        for zz in range(len(df)):
            llz=[]
            for z,i in df[zz].items():
                llz.append(str(i))
            lpp.append(llz)
        dic={}
        for i in range(len(df)):
            dic.update({str(i):lpp[i]})
        

        if str(to_predict_list['z'])=='e123' and str(to_predict_list['zs'])=='roman':
            name='Roman'
            
            df=pd.DataFrame.from_dict(dic, orient='index',columns=df[0].keys())
            df['情況']=df['情況'].replace('','處理中')
            df=df.drop(columns='世紀21經紀客人登記RomanTest_Id')
            df=df.loc[df.經紀姓名.str.contains(str(name),case=False)]
       
        elif str(to_predict_list['z'])=='e123' and str(to_predict_list['zs'])=='wilson':
            name='Wilson'
            df=pd.DataFrame.from_dict(dic, orient='index',columns=df[0].keys())
            df['情況']=df['情況'].replace('','處理中')
            df=df.drop(columns='世紀21經紀客人登記RomanTest_Id')
            df=df.loc[df.經紀姓名.str.contains(str(name),case=False)]
            
        else:
            df=pd.DataFrame({'None':['None']})
        return render_template("./result.html",tables=[df.to_html(classes='data')])


@app.route('/',methods = ['POST'])
def home1():
    if request.method == 'POST':
        return render_template("home.html")


if __name__ == "__main__":
    app.debug = True
  

    app.run(debug=True)


# class Solution:
#     def coinChange(self, coins, amount):
#         if amount < 0:
#             return - 1
#         dp = [[amount + 1 for _ in range(len(coins) + 1)]for _ in range(amount + 1)]
#         # 初始化第一行为0，其他为最大值（也就是amount + 1）

#         for j in range(len(coins) + 1):
#             dp[0][j] = 0

#         for i in range(1, amount + 1):
#             for j in range(1, len(coins) + 1):
#                 if i - coins[j - 1] >= 0:
#                     dp[i][j] = min(
#                         dp[i][j - 1], dp[i - coins[j - 1]][j] + 1)
#                 else:
#                     dp[i][j] = dp[i][j - 1]

#         return -1 if dp[-1][-1] == amount + 1 else dp[-1][-1]
# Solution().coinChange([1,3,5],11)
