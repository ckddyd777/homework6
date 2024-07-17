import streamlit as st
import json
from collections import Counter
import pandas as pd
import os

st.title('My First Streamlit App')

file1 = st.file_uploader("단어 개수를 셀 파일을 업로드 해주세요", type=['csv', 'txt'])
file2 = st.file_uploader("불용어를 제거하고 싶다면 파일을 업로드 해주세요", type=['csv', 'txt'])

# input.txt 파일이 업로드 되었는지 확인
if file1 is None:
    st.warning('파일이 업로드 되지 않았습니다.')
    st.stop()  # 업로드되지 않은 경우 함수 종료

# 업로드된 경우 추가 작업 수행
st.success('파일 업로드 완료!')

#file1_contents = file1.read().decode('utf-8')
#rint(file1_contents)
stopwords = set()
# stopwords.txt 파일이 업로드된 경우 추가 작업 수행
if file2 is not None:
    st.success('파일 업로드 완료!')
    stopwords = set(file2.read().decode('utf-8').splitlines())

text = file1.read().decode('utf-8')

words = text.split()
filtered_words = [word for word in words if word.lower() not in stopwords]
word_counts = Counter(filtered_words)

word_count_json = json.dumps(word_counts, ensure_ascii=False)
with open('/tmp/word_counts.json', 'w', encoding='utf-8') as f:
    f.write(word_count_json)

word_count_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])

st.download_button(
    label="결과 JSON 파일 다운로드",
    data=word_count_json,
    file_name='word_counts.json',
    mime='application/json'
    )

st.table(word_count_df.sort_values('Count', ascending=False).reset_index(drop=True))