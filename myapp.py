import streamlit as st
import requests
import pandas as pd

def main():
    url = 'http://10.40.98.74:20070/safety/v1/safe'
    st.set_page_config(page_title="Safety Test UI", page_icon="⚠️")
    st.title("Safety 모듈 검토해 봅시다!")
    session = requests.Session()
    with st.form("my_form"):
        index = st.text_input("문장", max_chars=150)
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                querystring_all = {"utterance":index, "min_len":0, "max_len":100, "early_stop":"false", "source": "user", "method": "all"}
                response_all = requests.request("GET", url, params = querystring_all)
                json_response_all = response_all.json()
                safe_all = json_response_all['result_body']['is_safe']
                stopwords_all = json_response_all['result_body']['stopword'][0]['text']
                method_all = json_response_all['result_body']['stopword'][0]['method']
                all_res = {'safe': str(safe_all), 'stopwords': stopwords_all, 'method': method_all}
                df_all = pd.DataFrame(data=all_res, index=[0])

                querystring_mdl = {"utterance":index, "min_len":0, "max_len":100, "early_stop":"false", "source":"user", "method":"mdl"}
                response_mdl = requests.request("GET", url, params = querystring_mdl)
                safe_mdl = json_response_all['result_body']['is_safe']
                stopwords_mdl = json_response_all['result_body']['stopword'][0]['text']
                method_mdl = 'model'
                mdl_res = {'safe': str(safe_mdl), 'stopwords': stopwords_mdl, 'method': method_mdl}
                df_mdl = pd.DataFrame(data=mdl_res, index=[0])
           
            except:
                print("다시 시도해 보세요 :(")
    
            st.write("# Safety 결과")
            if response_all:
                st.write(
                """
                ALL RESULT
                """)
                st.dataframe(df_all)
            
            if response_mdl:
                st.write(
                """
                MODEL RESULT
                """)
                st.dataframe(df_mdl)


if __name__ == '__main__':
    main()
