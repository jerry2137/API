import sys
import requests
import os
import csv
import pandas as pd


#create the destinated directory and store the data inside
def store(date, site, data_file):
  #-------------------------------------------------------------------------------------------
  all_file_path = 'data/'
  #-------------------------------------------------------------------------------------------
  date_path = all_file_path + date + '/'

  #wrong name
  if type(data_file) == str:
    return

  #create the directory if it does not exist
  if not os.path.isdir(all_file_path):
    os.mkdir(all_file_path)
  if not os.path.isdir(date_path):
    os.mkdir(date_path)
  
  #store the dataframe
  df = pd.DataFrame.from_dict(data_file)
  df.to_csv(date_path + site + '.csv', index=None)

#call store() to store all the site files
def store_sites(date, data_file):
  for site, data in data_file.items():
    store(date, site, data)

#call store() to store all the date files
def store_dates(site, data_file):
  for date, data in data_file.items():
    store(date, site, data)

#call store_sites() to store all the files
def store_all(data_file):
  for date, site_data in data_file.items():
    store_sites(date, site_data)

#download the required files
def download(start_date, site, end_date=''):
  #-------------------------------------------------------------------------------------------
  api_url = "http://10.10.12.24:5000/weather_data/"

  #put the abbreviation and full name of the sites into a dictioanry
  with open('names.csv', 'r') as name_file:
  #-------------------------------------------------------------------------------------------
    names = csv.reader(name_file)
    name_dict = {name[0] : name[1] for name in names}
  
  #load data  
  response = requests.get(os.path.join(api_url, start_date, end_date, site).replace('\\', '/'), allow_redirects=True)
  data_file = response.json()

  #http://127.0.0.1:5000/weather_data/all/
  if start_date == 'all':

    #http://127.0.0.1:5000/weather_data/all/all/ download all the data
    if site == 'all':
      store_all(data_file)
      return

    #http://127.0.0.1:5000
    # weather_data/all/cch/ download all the data from cch
    elif site in name_dict:
      store_dates(site, data_file)
      return

  #http://127.0.0.1:5000/weather_data/20220926/
  elif start_date.isdigit():

    #http://127.0.0.1:5000/weather_data/20220926/all/ download all the data on 20220926
    if site == 'all':
      store_sites(start_date, data_file)
      return

    #http://127.0.0.1:5000/weather_data/20220926//cch
    elif site in name_dict:
      
      #http://127.0.0.1:5000/weather_data/20220926/cch/ download the data on 20220926 from cch
      if end_date == '':
        store(start_date, site, data_file)
        return

      #http://127.0.0.1:5000/weather_data/20220926/20221001/cch download all the data on 20220926
      elif end_date.isdigit():
        store_dates(site, data_file)
        return

  #wrong name
  print('wrong name')


if __name__ == '__main__':
  #ignore the end_date if only one day or all dates
  if len(sys.argv) < 4:
    download(start_date=sys.argv[1], site=sys.argv[2])
  else:
    download(start_date=sys.argv[1], end_date=sys.argv[2], site=sys.argv[3])

  #download(start_date='20220926', end_date='20221001', site='cch')
