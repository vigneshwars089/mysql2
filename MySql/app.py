#vigneshwar selvaraj
#1001863627
#CSE 6331, Cloud Computing
#Assignment 4 

from flask import Flask, render_template, request
from numpy import place
app = Flask(__name__)
from time import time
import pyodbc 
import pandas as pd
import re as re
import string
import datetime as datetime
from dateutil.parser import parse 
import random
import json
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'vickwar.database.windows.net' 
database = 'First' 
username = 'vickwar' 
password = 'vickywar_IS' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

pf =pd.read_sql_query("select * from First.dbo.earthq where mag>=? and mag<=?",cnxn,params=(1,3))
pr =pd.read_sql_query("select * from First.dbo.earthq",cnxn)
cnxn.commit()
#magres=pf.loc[pf['mag'] == 5]
magres=pf
len=len(magres.index)
date_time_str="2021-06-13T20:41:44.940Z"
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')

def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

@app.route('/')
def student():  
   #pn=pf.head(1)
   pn=pf[['id','mag']]
   d=pn.values.tolist()
   c=pn.columns.tolist()
   d.insert(0,c)
   title = "Monthly Max and Min Temperature"
   tempdata=json.dumps({'title':title,'data':d})
   print(tempdata)
   #pn=pn.loc[,: ['country','year']].head()
   chart_data = pn.to_dict()
   #print(chart_data)
   #chart_data = json.dumps(chart_data, indent=2)
   #data = {'chart_data': chart_data}
   #data=chart_data
   #print(pn.to_numpy())
   new={}
   
   data = {'Task' : 'Hours per Day', 'Work' : 22, 'Eat' : 4, 'Commute' : 6, 'Watching TV' : 5, 'Sleeping' : 15}

   return render_template('student.html',tempdata=tempdata)


# @app.route("/thread")
# def get_graph_data():
#    pn=pf.head(1)
#    chart_data = pn.to_dict(orient='records')
#    chart_data = json.dumps(chart_data, indent=2)
#    data = {'chart_data': chart_data}
#    print(chart_data)
#    return chart_data


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':

      value= request.form['value']
      option = request.form['options']

      # tic = time()
      if option =='option1':

         querytime(int(value))
      else:
         querytime2(int(value))
      # toc = time()
      # now=toc-tic
      return render_template("result.html")


@app.route('/result2',methods = ['POST', 'GET'])
def result2():
   if request.method == 'POST':
      value= request.form['value']
      option = request.form['options']
      type = request.form['type']
      tic = time()
      if type=='ca':
         queryca(int(value),option)

      if type=='km':
         lat = request.form['lat']
         long = request.form['long']
         querykm(int(value),option,lat,long)


      if type=='mag':
         mag1 = request.form['magrange1']
         mag2 = request.form['magrange2']
         dfmag=querymag(mag1,mag2)

      
      #cnxn.commit()
      toc = time()
      now=toc-tic
      
      return render_template("result2.html",tables=[dfmag.to_html(classes='data')], titles=dfmag.columns.values)


def querytime(value):
   print(value)
   for val in range(value):
      rad=round(random.uniform(2.5, 7.0),2)
      print(rad)
      cursor.execute("""UPDATE First.[dbo].[earthq] SET mag=? WHERE net='nc'""",(rad))
      cnxn.commit()
   #time.sleep(60) 
   
def querytime2(value):
   for val in range(value):
      rad=round(random.uniform(2.5, 7.0),2)
      print(rad)
      cursor.execute(""" DELETE FROM First.[dbo].[earthq] WHERE mag='?' ASC LIMIT 1""",rad)
      cnxn.commit()

def queryca(value,option):
   for val in range(value):
      rad=round(random.uniform(2.5, 7.0),2)
      print(rad)
      if option =='option1':
        cursor.execute("""UPDATE First.[dbo].[earthq] SET mag=? WHERE net='nc' AND place LIKE '%, CA%'""",(rad))
      else:
         cursor.execute(""" DELETE FROM First.[dbo].[earthq] WHERE mag='?' AND place LIKE '%, CA%' ASC LIMIT 1""",rad)
      cnxn.commit()
   #time.sleep(60)
def querykm(value,option,lat,long):
   for val in range(value):
      rad=round(random.uniform(2.5, 7.0),2)
      print(rad)
      if option =='option1':
        cursor.execute("""UPDATE First.[dbo].[earthq] SET mag=? WHERE  latitude=? and longitude=?""",(rad,lat,long))
      else:
         cursor.execute(""" DELETE FROM First.[dbo].[earthq] WHERE latitude=? and longitude=? ASC LIMIT 1""",(rad,lat,long))
      cnxn.commit()
def querymag(mag1,mag2):
   
      #rad=round(random.uniform(2.5, 7.0),2)
      #print(rad)
      cursor1 = cnxn.cursor()
      sqlq="""SELECT Price FROM Laptop WHERE  mag>=? and mag<=?"""
      cursor1.execute(sqlq, (mag1,mag1,))
      #cursor.execute("""UPDATE First.[dbo].[earthq] SET mag=? WHERE  mag>=? and mag<=?""",(rad,mag1,mag2))
      dfmag = cursor1.fetchall()
         
      cnxn.commit()
      return dfmag
if __name__ == '__main__':
   app.run(debug = True)