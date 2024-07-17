import streamlit as st
import altair as alt
import requests
import pandas as pd
import json
from wordcount import WordFrequencyController
from datetime import datetime
import os
st.header('실습! 숙제를 streamlit으로')
df = pd.DataFrame()
if len(os.listdir('data/save')) > 0:
    json_list = [file for file in os.listdir('data/save')]
    df = pd.DataFrame({"File":json_list})
    

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)
selected_file = None
uploaded_file = None

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    filename = df.iloc[selected_row]['File']
    selected_file = 'data/save/' + filename
    st.write(selected_file)
# * optional kwarg unsafe_allow_html = True
uploaded_file = st.file_uploader(
    "Upload a file",
    type=("txt"),
    accept_multiple_files=True,
    key="upload2"
)
print("test")
if not uploaded_file and not selected_file:
    st.stop()

try:
    col1, col2 = st.columns([0.5, 0.5], gap='small')
    if len(uploaded_file) > 0:
        wfc = WordFrequencyController(uploaded_file)
        res = wfc.run()
        res.columns = ['Word', 'Count']
    elif selected_file:
        res = pd.read_json(selected_file)

    with col1:
        st.dataframe(res, use_container_width=True, height=600)
    with col2:
        chart = (
            alt.Chart(
                res,
                title="Data into chart",
            )
            .mark_bar()
            .encode(
                x=alt.X("Count", title="'Word counts in uploded file"),
                y=alt.Y(
                    "Word",
                    sort=alt.EncodingSortField(field="Count", order="descending"),
                    title="",
                ),
                tooltip=["Word", "Count"],
            )
        )
        st.altair_chart(chart, use_container_width=True)
    if st.button("JSON으로 저장하기"):
        print(uploaded_file)
        current_time = datetime.now()
        filename = current_time.isoformat().replace(':', "_") + '.json'
        res.to_json(f"data/save/{filename}", force_ascii=False)
        st.success('Save result to JSON file.')
        st.rerun()
    if st.button("DB에 저장하기"):
        pass
except Exception as e:
    print(e)
