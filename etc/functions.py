import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def format_date_for_comparison(date) -> float:
    if date[1]==2:  return float(date[2:]) + 0.25
    elif date[1]==3:    return float(date[2:]) + 0.5
    elif date[1]==4:    return float(date[2:]) + 0.75
    else: return float (date[2:])

def end_before_start(start_date, end_date) -> bool:
    num_start_date=format_date_for_comparison(date=start_date)
    num_end_date=format_date_for_comparison(date=end_date)

    return True if num_start_date>num_end_date else False

def display_dashboard(start_date, end_date, target,df:pd.DataFrame):
    tab1,tab2=st.tabs(tabs=["Population Change","Compare"])
    
    with tab1:
        tab1.subheader(body=f"Population Change from {start_date} to {end_date}")
        col1, col2=tab1.columns(spec=2)
        with col1:
            initial=df.loc[df['Quarter'] == start_date,target].item()
            final=df.loc[df['Quarter'] == end_date,target].item()
            percentage_diff=round(((final-initial)/initial)*100,2)
            delta=f"{percentage_diff}%"
            col1.metric(label=start_date, value=initial)
            col1.metric(label=end_date, value=final, delta=delta)
        with col2:
            start_idx=df.loc[df['Quarter']==start_date].index.item()
            end_idx=df.loc[df['Quarter']==end_date].index.item()
            filtered_df=df.iloc[start_idx:end_idx+1]

            fig,ax=plt.subplots()
            ax.plot(filtered_df['Quarter'], filtered_df[target])
            ax.set_xlabel("Time")
            ax.set_ylabel("Population")
            ax.grid()
            ax.set_xticks([
                filtered_df['Quarter'].iloc[0],
                filtered_df['Quarter'].iloc[-1]
                ]
            )
            fig.autofmt_xdate()
            col2.pyplot(fig=fig)
    
    with tab2:
        tab2.subheader(body="Compare with other locations")
        all_targets=tab2.multiselect(
            label="Choose Other Locations",
            options=df.columns[1:],
            default=[target]
            )
        fig.ax=plt.subplots()
        for each in all_targets:
            ax.plot(filtered_df['Quarter'],filtered_df[each])
        ax.set_xlabel("Time")
        ax.set_ylabel("Population")   
        ax.set_xticks([
            filtered_df['Quarter'].iloc[0],
            filtered_df['Quarter'].iloc[-1]
        ]) 
        tab2.pyplot(fig=fig)

