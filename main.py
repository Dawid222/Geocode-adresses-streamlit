import pandas as pd
import json
import requests
import streamlit as st
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
from streamlit_lottie import st_lottie
from time import sleep

col1, col2, col3 = st.columns([2, 6, 2])

with col2:
  st.title("Geocoding addresses")


  def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
      return json.load(f)


  def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
      return None
    return r.json()


  lottie_coding = load_lottiefile("75683-2-points-map-route.json")  # replace link to local lottie file
  lottie_hello = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_ug4q6zc4.json")

  st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",  # medium ; high
    height=400,
    width=400,
    key=None,
  )

col4, col5, col6 = st.columns([1, 8, 1])

with col5:
  st.markdown('Prepare the data according to the instructions, which can be downloaded below. ')

col7, col8, col9 = st.columns([4, 2, 4])

with col8:
  with open("Instruction.pdf", "rb") as pdf_file:
    pdf = pdf_file.read()

  st.download_button(
    "Download PDF",
    data=pdf,
    file_name='Instruction.pdf',
    mime='application/octet-stream',
  )

col10, col11, col12 = st.columns([1.5, 7, 1.5])
with col11:
  st.markdown('Upload your **CSV file** below and program start geocoding addresses')

uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
  #Progress bar
  col13, col14, col15 = st.columns([3.5, 3, 3.5])
  with col14:
    with st.spinner('Wait for it...'):
      time.sleep(5)
    st.success('Geocoding Successful!')
  #Geocoding
  df = pd.read_csv(uploaded_file)

  df["geocode"] =  df["ay"].map(str)  + ',' + df['ax'].map(str)

  locator = Nominatim(user_agent="myGeocoder", timeout=10)
  rgeocode = RateLimiter(locator.reverse, min_delay_seconds=0.001)
  #New columns in csv
  df['address_all'] = df['geocode'].apply(rgeocode)
  df['nr_house'] = df['address_all'].apply(
    lambda x: (x.raw['address']['house_number'] if 'house_number' in x.raw['address'].keys() else None))
  df['road'] = df['address_all'].apply(
    lambda x: (x.raw['address']['road'] if 'road' in x.raw['address'].keys() else None))
  df['city'] = df['address_all'].apply(
    lambda x: (x.raw['address']['city'] if 'city' in x.raw['address'].keys() else None))
  df['postcode'] = df['address_all'].apply(
    lambda x: (x.raw['address']['postcode'] if 'postcode' in x.raw['address'].keys() else None))
  df['country'] = df['address_all'].apply(
    lambda x: (x.raw['address']['country'] if 'country' in x.raw['address'].keys() else None))

  col16, col17, col18 = st.columns([3.5, 3, 3.5])

  with col17:
    def geocode_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
      return df.to_csv().encode('utf-8')

    csv = geocode_df(df)

    st.download_button(label='📥 Download data as CSV',
                                data = csv,
                                file_name = "large_df.csv",
                                mime = 'text/csv',
                     key='download-csv'
                  )

col19, col20, col21 = st.columns([3.5, 3, 3.5])

with col20:
  st.caption("Created by Dawid Bochnak")

col122, col23, col24 = st.columns([4.2, 1, 4.75])

with col23:
  st.write(
    """<div style="width:100%;text-align:center;"><a href="www.linkedin.com/in/dawid-bochnak" style="float:center"><img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" width="22px"></img></a></div>""",
    unsafe_allow_html=True)



