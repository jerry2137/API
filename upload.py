from flask import Flask
import os
import csv
import pandas as pd

#-------------------------------------------------------------------------------------------
#cwd = os.path.dirname(os.path.realpath(__file__))
#all_file_path = cwd + '/data/'
all_file_path = r"D:\test_development\Weather\Weather_update\data/"
#-------------------------------------------------------------------------------------------

#run API with Flask
app = Flask(__name__)

#home page
@app.route('/weather_data/')
def home():
  return 'Please enter the file name after the link. E.g., 10.10.12.24:5000/weather_data/20220926/wlp'

#upload all the data
@app.route('/weather_data/all/all/')
def all():
  all_files = {date : all_sites(date) for date in os.listdir(all_file_path)}
  return all_files

#upload all the data on the specific date
@app.route('/weather_data/<string:date>/all/')
def all_sites(date):
  #-------------------------------------------------------------------------------------------
  #put the abbreviation and full name of the sites into a dictioanry
  #with open('names.csv', 'r') as name_file:
  with open('D:/test_development/Weather/names.csv', 'r') as name_file:
  #-------------------------------------------------------------------------------------------
    names = csv.reader(name_file)
    
    files = {site[0] : specific(date, site[0]) for site in names}
  return files

#upload all the data on the specific site
@app.route('/weather_data/all/<string:site>/')
def all_dates(site):
  files = {date : specific(date, site) for date in os.listdir(all_file_path)}
  return files

#upload the data on the specific date range of the specific site
@app.route('/weather_data/<string:start_date>/<string:end_date>/<string:site>/')
def range(start_date, end_date, site):
  dates = [date.strftime('%Y%m%d') for date in pd.date_range(start = start_date, end = end_date, freq = '1D')]
  files = {date : specific(date, site) for date in dates}
  return files

#upload the data on the specific date of the specific site
@app.route('/weather_data/<string:date>/<string:site>/')
def specific(date, site):
  file_path = all_file_path + date + '/' + site + '_' + date + '.csv'

  if os.path.exists(file_path):
    df = pd.read_csv(file_path, names=['date', 'temperture', 'humidity'])
    return df.to_dict()
  return 'file not found'


if __name__ == '__main__':
  #run the API
  app.run(host='0.0.0.0', port='5000', debug=True)