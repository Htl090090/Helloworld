import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

#设置页面
st.set_page_config(page_title="螺栓应力寿命计算",layout="wide")

#添加标题
st.title('螺栓应力寿命计算')

#添加子标题以文件形式输入原始压力数据集
st.subheader('原始应力输入')

import math

def get_gd_list(list):
    ##函数开始时，定义了一个变量dq_rex并将其初始化为0，同时创建一个空列表gd_list用于存储波峰和波谷的元素。
    dq_rex = 0
    gd_list = []
    ##使用for循环遍历输入列表list中的元素。range(len(list))生成一个整数序列，范围是从0到list的长度减1。
    for i in range(len(list)):
        ###如果当前元素是最后一个元素（即i等于len(list) - 1），则将该元素添加到gd_list中，并用break语句终止循环。
        if i == len(list) - 1:
            gd_list.append(list[i])
            break
        ###在第一次循环时（即i等于0），首先计算相邻元素的差值（list[i+1] - list[i]），并将其赋值给dq_rex。将当前元素添加到gd_list中，继续下一次循环。
        if i == 0:
            dq_rex = list[i + 1] - list[i]
            gd_list.append(list[i])
            continue
        ###在之后的循环中，首先计算当前元素与下一个元素的差值，将其存储在变量rex中。
        rex = list[i + 1] - list[i]
        
     ##通过一系列条件判断来寻找波峰和波谷。
        ###如果rex大于0且dq_rex小于等于0，说明当前元素是一个波峰，将其添加到gd_list中，并更新dq_rex的值为rex，然后继续下一次循环。
        if rex > 0 and dq_rex <= 0:
            dq_rex = rex
            gd_list.append(list[i])
            continue
        ###如果rex小于0且dq_rex大于等于0，说明当前元素是一个波谷，将其添加到gd_list中，并更新dq_rex的值为rex，然后继续下一次循环。
        if rex < 0 and dq_rex >= 0:
            dq_rex = rex
            gd_list.append(list[i])
            continue
        ###如果rex等于0且dq_rex不等于0，说明当前元素是一个波峰或波谷，将其添加到gd_list中，并更新dq_rex的值为rex，然后继续下一次循环。
        if rex == 0 and dq_rex != 0:
            dq_rex = rex
            gd_list.append(list[i])
            continue
    return gd_list
##循环结束后，函数返回存储了波峰和波谷的gd_list列表。
#这一步是取拐点，我已经看明白了
def get_P_half(list_not_use):
    P_half = []
    ##遍历list_not_use列表中的元素
    for i in range(len(list_not_use)):
        ##在循环中，对每一对相邻元素进行计算，并将计算结果（相邻元素的差值的一半）添加到P_half列表中
        P_half.append(0.5*abs(list_not_use[i+1]-list_not_use[i]))
        ##检查是否到达了list_not_use列表的倒数第二个元素。如果到达了，即处理完了列表的所有元素，那么跳出循环
        if i+1 == len(list_not_use)-1:
            break
    return P_half



def pd_slope(data):
    # 直线上升直线下降返回true
    ##判断输入的列表data是否满足直线上升或直线下降的特性。如果列表中的所有元素按照顺序连续递增或连续递减，则函数返回True；否则，返回False
    if (all([data[i] < data[i + 1] for i in range(len(data) - 1)]) is True or
            all([data[i] > data[i + 1] for i in range(len(data) - 1)]) is True):
        return True
    return False

def get_Df(list):
    ##空列表，用于存储计算得到的结果。
    P_all = []
    P_half = []
    ##检查输入的列表list是否为空或长度是否小于4。如果满足这个条件，函数会立即返回0
    if list is None or len(list) < 4:
        return 0
    if pd_slope(list):
        #  取首尾求N半
        ##如果是连续递增或者递减，函数会将list的首尾元素传递给get_P_half函数，并将得到的结果赋值给P_half
        P_half = get_P_half([list[0], list[len(list)-1]])
    else:
        # 获取拐点数
        ##如果不是连续递增或者递减，调用get_gd_list,寻找波峰或者波谷,并存储在gd_list列表中
        gd_list = get_gd_list(list)
        
        
        ##
        list_not_use = []
        use_i = []
        ##遍历gd_list中的元素，从第二个元素开始，每隔一个元素进行一次循环
        for i in range(1, len(gd_list)-1, 2):
            ##果当前索引i+2大于等于gd_list的长度减1，即已经超出了列表的范围，跳出循环
            if (i + 2) > (len(gd_list)-1):
                break
            ##接下来的两个条件判断属于雨流判断法，如果满足条件，则将相应的数据加入P_all列表，并记录已使用的索引到use_i列表中
            if (gd_list[i - 1] < gd_list[i] <= gd_list[i + 2] and gd_list[i - 1] <= gd_list[i + 1]) or (
                    gd_list[i - 1] > gd_list[i] >= gd_list[i + 2] and gd_list[i - 1] >= gd_list[i + 1]):
                ##将波峰或波谷的高度差值的一半添加到P_all列表
                P_all.append(0.5 * abs(gd_list[i + 1] - gd_list[i]))
                ##将当前索引i和i+1添加到use_i列表中，表示这两个索引对应的波峰或波谷已经被使用
                use_i.append(i)
                use_i.append(i+1)
                continue
#这一步是取拐点，我已经看明白了
        ##遍历gd_list列表中的元素，创建一个名为flag的布尔变量，并将其初始化为False
        for i in range(len(gd_list)-1):
            flag = False
            ##遍历use_i列表（已经使用过的波峰和波谷的索引）中的元素
            for j in range(len(use_i)-1):
                ##条件判断，检查当前的索引i是否在use_i列表中。如果在，则将flag设置为True，表示当前的gd_list中的元素已经被使用过
                if i == use_i[j]:
                    flag = True
            ##条件判断，如果flag为False，即当前的gd_list中的元素未被使用过，则将该元素添加到list_not_use列表中
            if flag is False:
                list_not_use.append(gd_list[i])
        ##遍历结束后，函数会根据未使用的波峰和波谷的列表list_not_use来调用get_P_half函数，并将结果赋值给P_half
        P_half = get_P_half(list_not_use)
    return gd_list,P_all,P_half

def life(n,m):
    b = 0
    c=0

    for num in n:
        if num >= 49.9:
            a = 5 * (10 ** 6) * ((49.9/num)**3)
        else:
            a = 5 * (10 ** 6) * ((49.9/num)**3)
        
        b += 1/a
    for num in m:
        if num >= 49.9:
            a = 5 * (10 ** 6) * ((49.9/num)**3)
        else:
            a = 5 * (10 ** 6) * ((49.9/num)**3)
        
        c += 0.5/a
    d=c+b
    return d

def result(list):
    gd_list,P_all,P_half=get_Df(list)
    col_1,col_2 = st.columns((1,2))
    with col_1:
      st.header('波峰与波谷')
      st.write(pd.DataFrame({'波峰与波谷':gd_list}))
    with col_2:
      st.header('取拐点后的应力图')
      #st. line_chart( pd.DataFrame(gd_list))
      fig_2,ax_2 = plt.subplots(figsize=(6, 4), dpi= 80)
      # 设置图表标题和标签为中文
      plt.rcParams['font.sans-serif'] = ['SimHei']
      ax_2 = sns.lineplot( np.array(gd_list))
      plt.title('取拐点后的应力图',font='SimHei')
      x_major_locator=MultipleLocator(2)
      y_major_locator=MultipleLocator(200)
      plt.ylabel('压力值',font='SimHei')
      st.pyplot(fig_2)
    col_1,col_2 = st.columns(2)
    with col_1:
      st.header('全循环应力幅')
      st.write(pd.DataFrame({'全循环应力幅':P_all}))
    with col_2:
      st.header('半循环应力幅') 
      st.write(pd.DataFrame({'半循环应力幅':P_half}))

    st.header('疲劳寿命')
    st.write(life(P_all,P_half))

option = st.sidebar.radio(
 		      '原始压力输入方式选择',
		      ('直接键盘输入','文件输入')
		      )
if option == '文件输入':
 upload_file = st.file_uploader(
      label = "上传原始压力数据集CSV文件"
      )

 if upload_file is not None:
    df = pd.read_csv(upload_file) 
    st.success("上传文件成功")
 else: 
    st.stop()

 #显示图像
 st.subheader('原始压力折线图')
#画图
 #st. line_chart( pd.DataFrame(df['压力']))
 col_1,col_2 = st.columns((3,1))
 with col_1:
  sns.set_theme(style="white",
                font='Times New Roman',
                font_scale=1)  
  fig_1,ax_1 = plt.subplots(figsize=(6, 4), dpi= 80)
  ax_1 = sns.lineplot(df['压力'])
  plt.title('原始压力',font='SimHei')
  x_major_locator=MultipleLocator(2)
  y_major_locator=MultipleLocator(200)
  plt.ylabel('压力值',font='SimHei')
  st.pyplot(fig_1)

 with col_2:
  st.write(' ')


 df1=df['压力']
 list = df1.to_list()
 result(list)

else : 
  list = []
  str = st.text_input('原始应力输入',key='None')
  list1 = str.split(",")
  list = np.array(list1,dtype=np.int32)
  st.subheader('原始压力折线图')
  st. line_chart( pd.DataFrame(list))
  result(list)
