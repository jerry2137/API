import sys
import pandas as pd
import numpy as np
import pandas.io.formats.excel as excel
import os

#---------------------------------------------------------------------------------
import download
#---------------------------------------------------------------------------------


def extract(original_file_path, new_file_path, site_name):

    file_path = 'data/'
    
    df = pd.read_excel(original_file_path, index_col=False, header=0, skiprows=1)

    df_point = df.iloc[:1]
    df_data = df.iloc[1:]

    df_data['hour'] = df_data['*time'].astype(int)
    df_data['minutes'] = np.around((df_data['*time'] - df_data['hour']) * 60).astype(int)

    df_data['*To_db'] = np.nan
    df_data['RH'] = np.nan

    df_data = df_data.rename(columns = {'*Year':'year', '*Month':'month', '*Day_M':'day'})
    df_data['date'] = pd.to_datetime(df_data[['year','month','day', 'hour', 'minutes']], format = '%Y/%m/%d %H:%M')

    start_date = df_data['date'].iat[0].strftime('%Y%m%d')
    end_date = df_data['date'].iat[-1].strftime('%Y%m%d')
    download.download(start_date = start_date, end_date = end_date, site = site_name)
    
    weather_df = pd.concat([pd.read_csv(file_path + date_file + '/' + site_name + '.csv') for date_file in os.listdir(file_path)], ignore_index=True)

    weather_df['date']=pd.to_datetime(weather_df['date'], format='%Y/%m/%d %H:%M', infer_datetime_format=True)
    df_data=df_data.merge(weather_df[['date','temperture', 'humidity']],on='date',how='left')

    df_data['*To_db'] = df_data['*To_db'].fillna(df_data.pop('temperture'))
    df_data['RH'] = df_data['RH'].fillna(df_data.pop('humidity'))
    df_data = df_data.drop(['hour', 'minutes', 'date'], axis = 1)
    df_data = df_data.rename(columns = {'year':'*Year', 'month':'*Month', 'day':'*Day_M'})

    writer = pd.ExcelWriter(new_file_path, engine = 'xlsxwriter')

    excel.ExcelFormatter.header_style = None
    df_point.to_excel(writer, sheet_name='Sheet1', startrow = 0, index=False, header = False)
    df_data.to_excel(writer, sheet_name='Sheet1', startrow = 1, index=False, header = True)
    writer.save()


if __name__ == "__main__":
    extract(sys.argv[1] + '.xlsx', sys.argv[2] + '.xlsx', sys.argv[3])
    #extract('input/input_test.xlsx', 'input/output_test.xlsx', 'cch')
