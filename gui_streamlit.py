import streamlit as st
import json
import os
from main import select_article, replace

def show_result(article, inputs):
    article_replaced = replace(article['article'], inputs)
    st.info("最终的文章：")
    st.write(article_replaced)

def submit_answers():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_entry)

    args = {
        "file": file_path,
        "lang": language_var,
        "uid": article_var
    }

    if not os.path.isfile(args['file']):
        st.error("File Not Found: The specified file does not exist.")
        return

    article = select_article(args, main_data)

    user_input = [st.text_input(f"{hint}:") for hint in article['hints']]

    inputs = []
    for i in range(len(user_input)):
        inputs.append(user_input[i])

    st.button("查看结果", on_click=lambda: show_result(article, inputs))

def init():
    if 'state1' not in st.session_state:
        st.session_state['state1'] = False 

    st.title("Word Filling Game")

    global file_entry, language_var, article_var
    file_entry = st.text_input("题库路径：", value=main_args['file'])
    language_var = st.selectbox("选择语言：", options=['中文', 'English'], index=1 if main_args['lang'] == 'en' else 0)

    d = {'中文': 'zh', 'English': 'en'}
    max_value = len([article for article_group in main_data for article in article_group['articles'] 
                if d[language_var] == article_group['language']])
    article_var = st.slider("文章序号：", min_value=0, max_value=max_value-1, value=main_args['uid'])

    submit_button = st.button("提交")
    if submit_button:
        st.session_state['state1'] = True

    if st.session_state['state1']:
        submit_answers()


if __name__ == '__main__':

    if 'MAIN_ARGS' in os.environ and 'MAIN_DATA' in os.environ:
        main_args = json.loads(os.environ['MAIN_ARGS'])
        main_data = json.loads(os.environ['MAIN_DATA'])

    init()
