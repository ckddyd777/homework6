import streamlit as st
import pandas as pd
import json #딕셔너리와 유사하게 취급, 기본 자료형(문자열과 숫자)과 중첩 목록, 튜플 및 객체 지원
import sqlite3 #파이썬에서 SQLite 데이터베이스를 다룰 수 있는 모듈
from collections import Counter #데이터 개수 count시 사용
from typing import List, Dict, Tuple #타입별로 표기

# SQLite DB 연결
conn = sqlite3.connect('wordcount.db')
c = conn.cursor()

# 테이블 생성
c.execute('''
    CREATE TABLE IF NOT EXISTS word_count (
        file_name TEXT,
        word TEXT,
        count INTEGER
    )
''')
conn.commit()

# 파일 업로드 기능
st.title("Word Count 앱")

uploaded_files = st.file_uploader("input.txt 파일은 필수, stopword.txt는 선택사항", type=['txt'],
                                  accept_multiple_files=True)

# 업로드된 파일 분류
input_files = [file for file in uploaded_files if file.name == 'input.txt']
stopword_files = [file for file in uploaded_files if file.name == 'stopword.txt']

if not input_files:
    st.error("'input.txt'파일을 업로드 하세요.")
else:
    stopwords = set()
    if stopword_files:
        stopword_text = stopword_files[0].read().decode('utf-8')
        stopwords = set(stopword_text.split())


    # 단어 카운트 함수
    def count_words(file) -> List[Tuple[str, int]]:
        text = file.read().decode('utf-8')
        words = text.split()
        words = [word for word in words if word.lower() not in stopwords]
        word_count = Counter(words)
        return word_count.items()


    # 결과를 DB에 저장??????????
    for file in input_files:
        word_counts = count_words(file)
        c.executemany(
            'INSERT INTO word_count (file_name, word, count) VALUES (?, ?, ?)', #결과를 db에 파일명, 단어, 개수 순으로 저장?
            [(file.name, word, count) for word, count in word_counts]
        )
        conn.commit()

    st.success("Word counts 는 데이터 베이스에 저장되었습니다.")

    # DB에서 결과 읽기
    st.header("Word Count 결과")

    num_rows = st.number_input("표시할 행의 개수 : ", min_value=1, max_value=100, value=10, step=1)
    #value: 10 - 입력 필드의 기본값입니다. 초기에는 10개의 행이 표시되도록 설정됩니다.?
    #step: 1 - 사용자가 값을 증가시키거나 감소시킬 때 사용할 스텝(단위)입니다. 이 경우 1씩 증가하거나 감소합니다.

    result = pd.read_sql_query(f'SELECT * FROM word_count LIMIT {num_rows}', conn)
    # 쿼리한테 명령해서 읽어오는거?

    st.write(result)

    # JSON 파일로 저장
    if st.button("JSON 파일로 결과 저장"):
        result.to_json('word_count_results.json', orient='records')
        st.success("word_count_results.json로 저장되었습니다.")

# 연결 종료
conn.close()