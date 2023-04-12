######################
#import liblary
######################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import seaborn as sns
import streamlit as st
import re
import altair as alt

###################
#Title
###################
st.markdown("## 予測ツール")

##################
#data
#################
# file_type = st.sidebar.radio('実験データファイル形式',('csv','xlsx'))
# if file_type == 'csv':
#     w = st.sidebar.file_uploader("実験データアップロード", type = 'csv')
# elif file_type == 'xlsx':
#     w = st.sidebar.file_uploader("実験データアップロード", type = 'xlsx')
#

w = 'prediction_results_2023-03-28.csv'
data_all = pd.read_csv(w, index_col=0, encoding='utf-8')

data = data_all.copy()

col1, col2, col3, col4 = st.columns(4)
Polymer_Mn = col1.selectbox('Polymer_Mn',data['X01_Polymer_Mn'].unique(),index=0)
Pla_1 = col2.selectbox('Plasticizer_1',data['X02_Plasticizer_1'].unique(),index=0)
Pla_2 = col3.selectbox('Plasticizer_2',data['X03_Plasticizer_2'].unique(),index=0)
Fiber = col4.selectbox('Fiber',data['X04_Fiber'].unique(),index=0)

col1, col2, col3, col4 = st.columns(4)
Polymer_ratio = col1.selectbox('Polymer_ratio',data['X05_Polymer_ratio'].unique(),index=0)
Pla_1_ratio = col2.selectbox('Plasticizer_1_ratio',data['X06_Plasticizer_1_ratio'].unique(),index=0)
Pla_2_ratio = col3.selectbox('Plasticizer_2_ratio',data['X07_Plasticizer_2_ratio'].unique(),index=0)
#Fiber_ratio = col4.selectbox('Fiber_ratio',data['X08_Fiber_ratio'].unique(),index=0)
Fiber_ratio = 100 - (Polymer_ratio + Pla_1_ratio + Pla_2_ratio)
col4.metric('Fiber_ratio',Fiber_ratio)

col1, col2, col3, col4 = st.columns(4)
Temperature = col1.selectbox('Temperature',data['X09_Temperature'].unique(),index=0)

if st.button('Prediction!'):
    selected = data[
    (data['X01_Polymer_Mn'] == Polymer_Mn)&
    (data['X02_Plasticizer_1'] == Pla_1)&
    (data['X03_Plasticizer_2'] == Pla_2)&
    (data['X04_Fiber'] == Fiber)&
    (data['X05_Polymer_ratio'] == Polymer_ratio)&
    (data['X06_Plasticizer_1_ratio'] == Pla_1_ratio)&
    (data['X07_Plasticizer_2_ratio'] == Pla_2_ratio)&
    (data['X08_Fiber_ratio'] == Fiber_ratio)&
    (data['X09_Temperature'] == Temperature)
    ]

    col1,col2,col3,col4 = st.columns(4)
    col1.metric(label='Modulus',value=round(selected['Y01_Modulus']))
    col2.metric(label='Elongation',value=round(selected['Y02_Elongation']))
else:
    pass

visualize = st.checkbox('可視化',value=False)
if visualize:
    col1, col2 = st.columns(2)
    var1 = col1.selectbox('変数1(横軸)',c1_yX_inside_all.columns,index=0)
    var2 = col2.selectbox('変数2(縦軸)',c1_yX_inside_all.columns,index=1)

    col1, col2 = st.columns(2)
    number_of_filter = col1.number_input('フィルターを設定する変数の数',min_value=0,value=0)

    data_view_filtered = data_view_all.copy()

    for j in range(number_of_filter):
        col1, col2 = st.columns(2)
        filter_var = col1.selectbox('フィルター'+str(j),list(data_view_filtered.columns), key='filter'+str(j),index=j)
        if data_view_all[filter_var].dtype == 'object' or data_view_all[filter_var].dtype == 'bool':
            filter_candidate = sorted(data_view_all[filter_var].unique())
            filter = col2.multiselect(filter_var,filter_candidate,filter_candidate[0],key='multi_filter'+str(j))
            data_view_filtered = data_view_filtered[data_view_filtered[filter_var].isin(filter)]

        elif data_view_all[filter_var].dtype == 'float' or data_view_all[filter_var].dtype == 'int':
            range = col2.slider(filter_var, min_value = float(data_view_all[filter_var].min()), max_value = float(data_view_all[filter_var].max()), value=(float(data_view_all[filter_var].min()),float(data_view_all[filter_var].max())),key='slider_filter'+str(j))
            data_view_filtered = data_view_filtered[(data_view_filtered[filter_var]>=range[0])&(data_view_filtered[filter_var]<=range[1])]

    st.markdown('候補数 : '+ str(data_view_filtered.shape[0]))

    def plot_interactive(data,var_x,var_y):
        size = 10
        color = 'b'
        #tooltip_list =  sorted(list(set(data.columns[:10]) - set(var_x + var_y)))
        tooltip_list =  sorted(list(set(data.columns) - set(var_x + var_y)))
        chart = alt.Chart(data,height=500).mark_circle(size=200).encode(x=var_x, y=var_y, tooltip=tooltip_list, color = color)\
        .configure_axis(labelFontSize=16,titleFontSize=20)
        st.altair_chart(chart, use_container_width=True, theme=None)


    plot_interactive(data_view_filtered,var1,var2)

# if w:
#     ######################
#     #データ読み込み
#     #####################
#     if file_type == 'csv':
#         data_all = pd.read_csv(w, index_col=0, encoding='utf-8')
#     elif file_type == 'xlsx':
#         data_all_0 = pd.ExcelFile(w)
#         data_all = data_all_0.parse(data_all_0.sheet_names[0], index_col=0,header=0, encoding='shift-jis')
#         data_all_0.close()

    # #データセット
    # st.subheader('1_データセット読み込み')
    # st.dataframe(data_all)
    #
    # ################################
    # #データの概要を把握、使う変数の選択
    # #################################
    # st.write('データ概要')
    # st.dataframe(data_all.describe())
    #
    # st.markdown('---------------------------------------------------------------------')
    # st.subheader('2_変数選択')
    # selected_columns = st.multiselect('使う列',data_all.columns.tolist(),data_all.columns.tolist())
    #
    # data = data_all[selected_columns]
    #
    # qualitative_variable = st.multiselect('質的変数',selected_columns,selected_columns[0])
    #
    # quantitative_variable = sorted(set(selected_columns) - set(qualitative_variable),key = selected_columns.index)
    # quantitative_variable = st.multiselect('量的変数',quantitative_variable,quantitative_variable)
    #
    # st.markdown('---------------------------------------------------------------------')
    #
    # #################################
    # #データの概要を把握、使う変数の選択
    # #################################
    # st.subheader('3_変数変換')
    #
    # #対数変換
    # var_to_log = st.multiselect('対数変換する変数', quantitative_variable, None)
    # for l in var_to_log:
    #     if data[l].min()>0:
    #         data['log_'+l] = np.log(data[l])
    #     elif data[l].min()>0:
    #         min = data[data[l]>0][l].min()
    #         data['log_'+l] = np.log(data[l]+min)
    #
    #     quantitative_variable = quantitative_variable + ['log_'+l]
    #
    #
    # #ダミー変換
    # get_dummy = st.checkbox('ダミー変数にするか',value=True)
    # if get_dummy:
    #     dummy_var = st.multiselect('ダミー化する変数', qualitative_variable, qualitative_variable)
    #     data_dummied = pd.get_dummies(data.loc[:,dummy_var])
    #     dataset = pd.concat([data[quantitative_variable],data_dummied],axis=1)
    #
    #
    # st.dataframe(dataset)
    #
    # st.markdown('---------------------------------------------------------------------')
    #
    # #################################
    # #可視化
    # #################################
    # st.subheader('4_可視化')
    #
    # #相関プロット
    # plt.rcParams['font.size'] = 5
    # fig, ax = plt.subplots(figsize=(6, 6))  #図の大きさ
    # sns.heatmap(dataset.corr(), vmax=1, vmin=-1, cmap='seismic', square=True, annot=True, xticklabels=1, yticklabels=1, ax=ax)
    # st.pyplot(fig)
    #
    #
    # #散布図（altair_chart）
    # dataset.insert(0,'Index',dataset.index)
    #
    # col1, col2 = st.columns(2)
    # var1 = col1.selectbox('変数1',data.columns,index=0)
    # var2 = col2.selectbox('変数2',data.columns,index=1)
    #
    # size = 10
    # color = 'b'
    #
    # tooltip_list =  sorted(list(set(data.columns[:10]) - set(var1 + var2)))
    #
    # chart = alt.Chart(data,height=500).mark_circle(size=200).encode(x=var1, y=var2, tooltip=tooltip_list)\
    # .configure_axis(labelFontSize=16,titleFontSize=20)
    #
    # col1,col2,col3 = st.columns([0.15,1,0.2])
    # with col2:
    #     st.altair_chart(chart, use_container_width=True, theme=None)
