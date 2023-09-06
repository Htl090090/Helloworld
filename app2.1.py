import streamlit as st
import pickle
import pandas as pd
from pandas import DataFrame
import pickle
import time
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import MultipleLocator
import matplotlib.font_manager as fm

font1 = FontProperties(fname=r'simhei.ttf')

st.session_state.date_time=datetime.datetime.now() + datetime.timedelta(hours=8)

st.set_page_config(page_title="生物质蒸汽气化气体产物预测",layout="wide",initial_sidebar_state="auto")
st.sidebar.radio("请选择功能：👇",
    ('工况预测', '影响规律预测'))
d=st.sidebar.date_input('Date',st.session_state.date_time.date())
t=st.sidebar.time_input('Time',st.session_state.date_time.time())
t=f'{t}'.split('.')[0]
st.sidebar.write(f'The current date time is {d} {t}')

st.title("生物质蒸汽气化气体产物预测")
st.header("")
aim = st.radio(
    "您的预测目标是：👇",
    ('产物浓度', '气化效率', '碳转化率'))

if aim == '产物浓度':
    model = pickle.load(open("H21.dat","rb"))

elif aim == '气化效率':
        st.write("You didn\'t select comedy.")
else:
        st.write("You didn\'t select comedy.")


with st.form('user_input'):
    # ash
    A = st.number_input(
        label = "灰分含量(A)",value=5.00,step=1.00,
        min_value = 0.00,max_value=50.00)
    # ② FC
    FC= st.number_input(
        label = "固定碳含量 (FC) ",value=25.00,step=1.00,
        min_value = 0.00,max_value=30.00)
    # ③VM
    V= st.number_input(
        label = "挥发分含量 (V) ",value=70.00,step=1.00,
        min_value = 45.00,max_value=90.00)
    # ③C
    C = st.number_input(
        label = "碳元素含量 (C) ",key=1,value=55.00,step=1.00,
        min_value = 25.00,max_value=60.00)
    # ③C
    H= st.number_input(
        label = "氢元素含量 (H) ",value=5.00,step=1.00,
        min_value =0.00,max_value=10.00)
    # ② FC
    O= st.number_input(
        label = "氧元素含量 (O) ",value=30.00,step=1.00,
        min_value = 15.00,max_value=50.00)
    # ③C
    ER = st.number_input(
        label = "氧气当量比 (ER) ",step=0.01,
        min_value = 0.00,max_value=0.50)
    # ⑤ T
    T = st.number_input(
        label = "反应温度(T)",value=800,step=10,
        min_value = 600,max_value=1000
    )
    # ⑥SB
    SB= st.number_input(
        label = "生物质与水蒸气质量比(S/B) ",value=1.00,step=0.10,
        min_value = 0.00,max_value=5.00
    )
    # 提交按钮
    submitted1 = st.form_submit_button('提交: 进行产气含量预测')
    if submitted1:
        st.write("用户输入的特征数据：{}".format([A, FC, V, C, H, O, ER, T, SB]))


        # 将所有特征合并起来
        temp_feature = [(A, FC, V, C, H, O, ER, T, SB)]
        data_frame = DataFrame(temp_feature,index=None,columns = ['A', 'FC', 'V', 'C', 'H', 'O', 'ER', 'T', 'SB'])
        # 模型预测
        new_prediction = model.predict(data_frame)

        # 根据模型的特征重要性输出，绘制特征：bill length, bill depth, flipper length 的直方图
        st.subheader("预测的氢气组分含量是：:red[{}]  %".format(new_prediction))

        
st.title("生物质蒸汽气化关键因素影响规律预测")
st.header("")
with st.form('data_input'):
 option1 = st.radio(
    "您选择的关键因素是：👇",
    ('反应温度', '氧气当量比', '水蒸气与生物质质量比'))
 aa=st.number_input(
        label = "工况1",step=1.00,
        min_value =0.00,max_value=1000.00)
 ab=st.number_input(
        label = "工况2",step=1.00,
        min_value =0.00,max_value=1000.00)
 ac=st.number_input(
        label = "工况3",step=1.00,
        min_value =0.00,max_value=1000.00)
 ad=st.number_input(
        label = "工况4",step=1.00,
        min_value =0.00,max_value=1000.00)
 ae=st.number_input(
        label = "工况5",step=1.00,
        min_value =0.00,max_value=1000.00)
 # 提交按钮
 submitted = st.form_submit_button('提交：不同工况数据确认')
 if submitted:
  parameters = {
    '反应温度': {
        'a1': 0.15,
        'a2': 0.15,
        'a3': 0.15,
        'a4': 0.15,
        'a5': 0.15,
        'b1': aa,
        'b2': ab,
        'b3': ac,
        'b4': ad,
        'b5': ae,
        'c1': 1,
        'c2': 1,
        'c3': 1,
        'c4': 1,
        'c5': 1,
        'd1': aa,
        'd2': ab,
        'd3': ac,
        'd4': ad,
        'd5': ae
     },
     '氧气当量比': {
        'a1': aa,
        'a2': ab,
        'a3': ac,
        'a4': ad,
        'a5': ae,
        'b1': 800,
        'b2': 800,
        'b3': 800,
        'b4': 800,
        'b5': 800,
        'c1': 1,
        'c2': 1,
        'c3': 1,
        'c4': 1,
        'c5': 1,
        'd1': aa,
        'd2': ab,
        'd3': ac,
        'd4': ad,
        'd5': ae
     },
     '水蒸气与生物质质量比': {
        'a1': 0.15,
        'a2': 0.15,
        'a3': 0.15,
        'a4': 0.15,
        'a5': 0.15,
        'b1': 800,
        'b2': 800,
        'b3': 800,
        'b4': 800,
        'b5': 800,
        'c1': aa,
        'c2': ab,
        'c3': ac,
        'c4': ad,
        'c5': ae,
        'd1': aa,
        'd2': ab,
        'd3': ac,
        'd4': ad,
        'd5': ae
     }
  }

  if option1 in parameters:
    params = parameters[option1]
    a1, a2, a3, a4, a5 = params['a1'], params['a2'], params['a3'], params['a4'], params['a5']
    b1, b2, b3, b4, b5 = params['b1'], params['b2'], params['b3'], params['b4'], params['b5']
    c1, c2, c3, c4, c5 = params['c1'], params['c2'], params['c3'], params['c4'], params['c5']
    d1, d2, d3, d4, d5 = params['d1'], params['d2'], params['d3'], params['d4'], params['d5']
  else:
    print("无效选项")

  data_predict1=([4.453156,17.826622,76.977467,48.354889,5.789244,40.194178,a1,b1,c1],
      [4.453156,17.826622,76.977467,48.354889,5.789244,40.194178,a2,b2,c2],
      [4.453156,17.826622,76.977467,48.354889,5.789244,40.194178,a3,b3,c3],
      [4.453156,17.826622,76.977467,48.354889,5.789244,40.194178,a4,b4,c4],
      [4.453156,17.826622,76.977467,48.354889,5.789244,40.194178,a5,b5,c5])

  df_predict1=pd.DataFrame(data_predict1,columns= ['A', 'FC', 'V', 'C', 'H', 'O', 'ER', 'T', 'SB'])

  new_prediction1 = model.predict(df_predict1)
  dataprediction = {'Name':new_prediction1}
  index = [d1, d2, d3, d4, d5]
  df = pd.DataFrame(dataprediction, index=index)

  # 定义要使用的字体
  custom_font = fm.FontProperties(fname='Times New Roman.ttf')

  # 设置Seaborn样式
  sns.set_theme(style="whitegrid", font=custom_font.get_name())
  sns.set_context("poster")
  plt.rcParams['font.family'] = custom_font.get_name()

  # 创建图形和坐标轴
  fig, ax = plt.subplots(figsize=(10, 6), dpi=80)

  # 绘制折线图
  sns.lineplot(data=df, x=df.index, y='Name', marker='o', markersize=8, color='b')

  # 设置Y轴刻度范围
  plt.ylim(0, max(df['Name']) * 1.2)

  #y轴间距
  y_major_locator=MultipleLocator(10)
  ax.yaxis.set_major_locator(y_major_locator)

  # 添加数据标签
  for x, y in zip(df.index, df['Name']):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', fontsize=14)

  # 设置刻度线的可见性
  ax.xaxis.set_visible(True)
  ax.yaxis.set_visible(True) 

  # 添加标题和坐标轴标签
  plt.title('关键影响因素与产气中氢气含量的关系图', fontproperties=font1, fontsize=20)
  plt.xlabel('影响因素', fontproperties=font1, fontsize=16)
  plt.ylabel('产气含量预测', fontproperties=font1, fontsize=16)

  # 设置坐标轴标签字体大小和粗细
  ax.tick_params(axis='x', labelsize=12)
  ax.tick_params(axis='y', labelsize=12)


  # 调整图形的边距
  fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)


  # 添加图例
  plt.legend(['氢气含量'],  loc='best', prop=font1, frameon=False, fontsize=10)

  # 设置网格线样式为虚线，并添加刻度
  ax.grid(linestyle='dashed')

  # 修改坐标轴刻度
  #plt.yticks(fontproperties=font, fontsize=10, rotation=45)

  #df_predict11=pd.DataFrame{([d1,d2,d3],new_prediction1),}
  #submitted1 = st.form_submit_button('提交: 进行规律预测')
  #if submitted1:
  st.write("用户输入的特征数据：{}".format([d1,d2,d3,d4,d5]))
  #st.line_chart(dff)  
  st.pyplot(fig)
