import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
from etc.functions import (end_before_start, display_dashboard)

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

df=pd.read_csv(filepath_or_buffer=URL,
               dtype={
                   "Quarter": str,
                   'Canada': np.int32,
                   'Newfoundland and Labrador': np.int32,
                   'Prince Edward Island': np.int32,
                   'Nova Scotia': np.int32,
                   'New Brunswick': np.int32,
                   'Quebec': np.int32,
                   'Ontario': np.int32,
                   'Manitoba': np.int32,
                   'Saskatchewan': np.int32,
                   'Alberta': np.int32,
                   'British Columbia': np.int32,
                   'Yukon': np.int32,
                   'Northwest Territories': np.int32,
                   'Nunavut': np.int32
               })

st.title(body="Population of Canada")

st.markdown(body="Source table can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")


with st.expander(label="See Sample Dataset Here"):
    st.dataframe(data=df.sample(n=100,random_state=20).sort_index())

with st.form(key="Population-Form"):
    col1, col2, col3=st.columns(spec=3)

    with col1:
        col1.write("Chose a Starting Date")
        start_quarter=col1.selectbox(label="Quarter",
                                   options=["Q1","Q2","Q3","Q4"],
                                   index=2,
                                   key="start_quarter"
                                   )
        start_year=col1.slider(label="Year",
                               min_value=1991,
                               max_value=2023,
                               step=1,
                               key="start_year"
                               )
        
    with col2:
        col2.write("Chose an End Date")
        end_quarter=col2.selectbox(label="Quarter",
                                   options=["Q1","Q2","Q3","Q4"],
                                   index=0,
                                   key="end_quarter"
                                   )
        end_year=col2.slider(label="Year",
                               min_value=1991,  
                               max_value=2023,
                               step=1,
                               key="end_year"
                               )
    
    with col3:
        col3.write("Choose a Location")
        target=col3.selectbox(label="Choose a Location",
                            options=df.columns[1:],
                            index=0,
                            key="location"
                            )
    
    submit_button=st.form_submit_button(label="Analyze")

    start_date=f"{start_quarter} {start_year}"
    end_date=f"{end_quarter} {end_year}"


if start_date not in df['Quarter'].tolist() or end_date not in df['Quarter'].to_list():
    st.error(body="Please check your Start Date and End Date Selection")
elif end_before_start(start_date=start_date,end_date=end_date):
    st.error(body="Start Date must come before end date")
else:
    display_dashboard(start_date=start_date, end_date=end_date, target=target, df=df)