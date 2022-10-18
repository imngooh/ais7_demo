import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import plotly.express as px

# 공식사이트 참고, 자동차 연비 테이블이 존재하는 페이지 만들어보기
# 한줄한줄 의미를 파악하며 만들어보는 것이 좋겠지! 그렇게 했다.

st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state= 'expanded'
)

st.markdown('# 자동차 연비🚗')
st.sidebar.markdown('# 자동차 연비🚗')

URL = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv'


@st.cache
def load_data(URL):
    return pd.read_csv(URL)


data_load_state = st.text('loading data...')
data = load_data(URL)

data_load_state.text('Load Done! (by using st.cache)') 
# 아까 그 text 자리에 있는 텍스트 바꾸어줌

st.markdown('## 전체 데이터')
data

# sidebar 만들기

st.sidebar.header("User Input Features")

selected_model = st.sidebar.selectbox('name', list(data.name.unique()))

start_year = st.sidebar.selectbox('Start Year', list(range(data.model_year.min(), data.model_year.max())))
end_year = st.sidebar.selectbox('End Year', list(reversed(range(data.model_year.min(), data.model_year.max()))))

selected_year = range(start_year, end_year + 1)

sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('orgin', sorted_unique_origin, sorted_unique_origin)




if len(selected_year) > 0 :
    selected_data = data[data.model_year.isin(selected_year)]
    
if len(selected_origin) > 0:
    selected_data = selected_data[selected_data.origin.isin(selected_origin)]
    
if bool(selected_model):
    selected_data = selected_data[selected_data.name == selected_model]
    
st.markdown('## 검색 결과 데이터')
st.dataframe(selected_data)




st.markdown('## 그래프')

pxhist = px.histogram(data, x='origin',title='지역별 연비 데이터 수')
st.plotly_chart(pxhist)

fig, axes = plt.subplots()
sns.barplot(data = data, x='origin', y='mpg').set_title('지역별 자동차 연비')
plt.tight_layout()
st.pyplot(fig)

st.line_chart(selected_data['mpg'])

st.bar_chart(selected_data['mpg'])

# 나만의 그래프 그려보기 그래 한번 그려보자 뭘 그려볼까
st.bar_chart(data=data, x='name', y='mpg')

fig2, axes = plt.subplots()
sns.barplot(data = data, x='cylinders', y='mpg', hue = 'origin', ci=None).set_title('지역 및 기통 별 연비')
st.pyplot(fig2)

# 참 다양한 그래프가 있는데 왜 맨날 bar만 생각나는지 원! 그리고 집계!
# raw data에 대한 그래프를 그리는 연습을 좀 해야한다. 분명히!

fig3, axes = plt.subplots()
sns.scatterplot(data = data, x='weight', y='mpg', hue = 'cylinders', palette = 'rainbow').set_title('mpg VS cylinders')
st.pyplot(fig3)

fig4, axes = plt.subplots()
sns.violinplot(data=data, x='cylinders', y='mpg').set_title('mpg per cylinders')
st.pyplot(fig4)
