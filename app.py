import pandas as pd
import requests
import os
import streamlit as st
from bokeh.plotting import figure


API_key=os.environ.get('ALPHA_VANTAGE_API')

symbol='GOOG'

url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(
    symbol,API_key)
data=requests.get(url).json()

df=pd.DataFrame(data['Time Series (Daily)']).transpose()
df=df.reset_index()
df=df.rename(columns={'index':'date'})
df['year']=[x[0:4] for x in df['date']]
df['month']=[x[5:7] for x in df['date']]
df['day']=[x[-2:] for x in df['date']]

month='08'
year='2021'

month_dict={'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
            '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

restrict=(df['month']==month)&(df['year']==year)

x=df['day'][restrict].astype(int)
y=df['5. adjusted close'][restrict].astype(float)


st.title('TDI 12-day Milestone Stock Price App')

p=figure(title='{} in {} {}'.format(symbol,month_dict[month],year),x_axis_label='Day',y_axis_label='Close (adjusted)')
#p.line(x,y,line_width=3)
p.line([0,1,2,3],[5,7,12,9],line_width=3)

st.bokeh_chart(p)