import streamlit as st
import altair as alt
import requests
import pandas as pd
from wordcount import WordFrequencyController
#import plotly.express as px
#import plotly.graph_objects as go
import os


st.header('Word Count_Streamlit')

# * optional kwarg unsafe_allow_html = True
uploaded_files = st.file_uploader(
    "파일 업로드(.txt)",
    type=("txt"),
    accept_multiple_files=True
)

stopwords = []
stopwords_file = st.file_uploader("stopword.txt 파일 업로드(필수x)", type="txt")
if stopwords_file:
    stopwords = stopwords_file.read().decode('utf-8').splitlines()


if not uploaded_files:
    st.stop()

try:
    for uploaded_file in uploaded_files:
        if os.path.splitext(uploaded_file)[1] == "txt":
            col1, col2 = st.columns([0.5, 0.5], gap='small')
            wfc = WordFrequencyController(uploaded_file)
            res = wfc.run()
            res.columns = ['Word', 'Count']
            with col1:
                st.dataframe(res, use_container_width=True)
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
except Exception as e:
    print(e)