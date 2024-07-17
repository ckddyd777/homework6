import streamlit as st
import pandas as pd
import json
import sqlite3
import sys 
from collections import Counter


conn = sqlite3.connect('word_count.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS WordCount(word TEXT, count INTEGER)")
conn.commit()

def main():
    st.title('파일 업로드하기')
    st.text('단어 수를 셀 파일을 업로드하세요')
    upload_files = st.file_uploader('파일 업로드하기', type =['txt'], accept_multiple_files=True)
    # upload_file = st.file_uploader('파일 업로드하기', type =['txt'])
    stop_file = st.file_uploader('제외할 단어 업로드하기', type =['txt'])  
    
    if upload_files:
        stop_word = stop_file.read().decode('utf-8').split()
        stops = set(stop_word)  
        
        for file in upload_files:
            words = file.read().decode('utf-8').split()
            words = [word if word.lower() not in stops else '' for word in words]
            word_count = Counter(words)

        c.execute('DELETE FROM WordCount')
        for word, count in word_count.items():
            c.execute("INSERT INTO WordCount (word, count) VALUES (?, ?)", (word, count))
        conn.commit()

        with open('f{file.name}_word_count.json', 'w') as json_file:
            json.dump(word_count, json_file)


    # if upload_file:
    #     stop_word = stop_file.read().decode('utf-8').split()
    #     stops = set(stop_word)  

    #     words = upload_file.read().decode('utf-8').split()
    #     words = [word for word in words if word.lower() not in stops]
    #     word_count = Counter(words)

    #     c.execute('DELETE FROM WordCount')
    #     for word, count in word_count.items():
    #         c.execute("INSERT INTO WordCount (word, count) VALUES (?, ?)", (word, count))
    #     conn.commit()

    #     with open('f{upload_file.name}_word_count.json', 'w') as json_file:
    #         json.dump(word_count, json_file)


if __name__ == '__main__':
    main()


rows_to_display = st.number_input("표시할 행 수 선택하기", min_value=1, max_value=1000, value=10)    

if st.button("단어 수 세기"):
    df = pd.read_sql_query(f"SELECT distinct word, count FROM WordCount ORDER BY count desc LIMIT {rows_to_display}", conn)
    st.dataframe(df)

