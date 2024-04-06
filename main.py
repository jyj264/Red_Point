# -*- coding:utf-8 -*-
import numpy.random
import streamlit as st
import json
import time
from urllib.request import urlopen
import requests
import numpy as np
import pandas as pd
import random
from matplotlib import pyplot as plt
from matplotlib import font_manager
import os

df = pd.DataFrame(columns=['lat', 'lon'])

def getlng(address):
    url='http://api.map.baidu.com/geocoding/v3'
    output='json'
    ak='dbEG8T1x1ZfY7sqwJJAL9SoO7pmUGYk5'
    uri="http://api.map.baidu.com/geocoding/v3?address="+address+"&output=json&ak=dbEG8T1x1ZfY7sqwJJAL9SoO7pmUGYk5&callback=showLocation%20//GET%E8%AF%B7%E6%B1%82"
    res=requests.get(uri).text
    temp=json.loads(res)
    lng=temp['result']['location']['lng']
    return lng

def change_text_color(text, color,size):
    return f'<p style="color: {color};font-size:{size}px;font-weight: 700;">{text}</p>'

def decimal_to_dms(decimal_number):
    # 整数部分
    degrees = int(decimal_number)
    # 小数部分乘以60，并取整得到分
    minutes = int(abs(decimal_number - degrees) * 60)
    # 再次乘以60，并取分数部分得到秒
    seconds = round(abs(decimal_number - degrees - minutes / 60) * 3600)

    return [degrees,minutes,seconds]

def get_current_location():
    headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
    }
    response = requests.get('https://ipapi.co/json/',headers=headers)
    data = response.json()
    st.info(data)
    return data['latitude'], data['longitude'],data

def getlat(address):
    url='http://api.map.baidu.com/geocoding/v3'
    output='json'
    ak='dbEG8T1x1ZfY7sqwJJAL9SoO7pmUGYk5'
    uri=url+'?'+'address='+address+'&output='+output+"&ak="+ak+'&callback=showLocation%20'+'//GET%E8%AF%B7%E6%B1%82'
    res = requests.get(uri).text
    temp = json.loads(res)
    lat = temp['result']['location']['lat']
    return lat

st.title("📌上海市红色文化景点导览系统")
tab2, tab3, tab1, tab4 = st.tabs(["首页", "添加", "关于", "帮助"])
with tab1:
    st.write("上海市红色文化景点导览系统 版本：0.2（由Python编写）")
    st.write("图形界面：Streamlit")
    try:
        a = pd.read_excel('RedPoint_AddressData.xlsx')
    except:
        st.error("源文件不存在或命名错误！")
        st.info("请点击“清空/复位”以创建数据文件")
    k = st.button('清空/复位')
    st.info("地址信息文件(.xlsx)存储于main.py所在的目录下，请勿删除或重命名，否则将会丢失所有数据！")
    if k:
        a = pd.DataFrame(columns=["Name", "lat","lon","Intro","Color","People","Name_en"])
        a.to_excel('RedPoint_AddressData.xlsx', index=False)
        st.success("操作成功！")
        time.sleep(0.4)
        st.rerun()
with tab2:
    if st.button("刷新地图"):
        try:
            with st.spinner("Loading……"):
                df = pd.read_excel('RedPoint_AddressData.xlsx')
                a=pd.DataFrame(columns=["Name","People"])
                a["Name"]=df["Name"]
                a["People"]=df["People"]
                for i in a.index:
                    a["People"][i]=a["People"][i]+random.randint(-50,50)
                plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
                plt.rcParams['axes.unicode_minus'] = False
                fig, ax = plt.subplots()

                # 绘制柱状图，并通过color参数设置颜色，通过linewidth参数设置粗细
                ax.bar(df['Name_en'], a['People'], color=df["Color"], linewidth=2)
                st.title("模拟景点客流量")
                ax.set_ylabel('People')
                ax.set_title('')
                plt.xticks(rotation=90)
                # 使用Streamlit的st.pyplot函数显示图表
                st.pyplot(fig)
                st.title("景点分布图")
                st.map(df,color="Color")
                st.title("景点介绍")
            for i in df.index:
                if df["Name"][i]!="Current":
                    text = df["Name"][i]
                    color = df["Color"][i]
                    size=40
                    colored_text = change_text_color(text, color,size)

                    # 显示带有颜色的文本
                    st.markdown(colored_text, unsafe_allow_html=True)
                    st.markdown(df['Intro'][i])
                    st.image(df["Name"][i]+".webp", use_column_width=True)
        except AttributeError:
            st.error("没有与搜索条件所匹配的项目，请重新输入")
        except PermissionError:
            st.error("该文件正在被使用，无法访问，请关闭正在使用此程序的软件！")
with tab3:
    try:
        a = pd.read_excel('RedPoint_AddressData.xlsx')
        address = st.text_input("请输入地标所在的具体位置：",key=222)
        en=st.text_input("请输入地标英文名：",key=7777)
        intro = st.text_input("请输入该地标的介绍:",key=333)
        color = st.color_picker("请选择地标标志色:",key=3333)
        picture =st.file_uploader("请上传地标图片:",type="webp")
        if st.button("保存"):
            try:
                if a["Name"].isin([address]).sum() != 0:
                    st.warning("地点已经存在，不可添加！请您重新输入")
                else:
                    # 示例使用
                    latitude = getlat(address)-0.0035
                    longitude = getlng(address)-0.0103
                    a=a._append({'Name':address,'lat':latitude,'lon':longitude,'Intro':intro,'Color':color,'People':random.randint(100,9999),"Name_en":en},ignore_index=True)
                    a.to_excel('RedPoint_AddressData.xlsx', index=False)
                    bytes_data = picture.read()
                    with open(address+".webp", "wb") as file:
                        file.write(bytes_data)
                    st.success("上传成功！")
                    st.success("数据保存成功！")
            except KeyError:
                st.error("无相关结果")
    except AttributeError:
        st.error("源文件不存在或命名错误！")
        st.info("请点击“清空/复位”以创建数据文件")
with tab4:
    st.title("软件介绍")
    st.markdown(''' “上海市红色文化景点导览系统”旨在为用户展示上海市内的红色文化景点，并通过互动式的地图和详细的景点介绍，增强公众对这些重要历史遗址的认识和理解，传播红色文化。该系统已经成功在Streamlit的公有云上完成部署。用户可以通过访问网址 https://redpoints.streamlit.app/ 来体验这一系统的功能。
该系统使用Python编写，Python语言的Streamlit库提供网站图形界面服务。核心功能包括在地图上标记上海市的红色文化景点、提供每个景点的详细介绍与图片，还允许用户添加新的景点信息，让每个人都能为传播上海的红色文化贡献自己的力量。通过这一系统，用户可以轻松地找到并了解上海市内的主要红色文化景点，包括但不限于历史事件的发生地、重要人物的纪念场所以及具有特殊意义的文化地标。
在地图显示方面，系统采用了将红色文化景点以有颜色的点的形式清晰地标注在地图上，用户可以通过寻找与点的颜色相同的标题来获取每个景点的具体位置和相关信息。这不仅方便了用户的导航和访问，也使得用户能够更加直观地了解上海市红色文化景点的分布情况。
景点介绍部分则为用户提供了详尽的信息，包括景点的历史背景、文化价值等。这些信息的提供，不仅有助于用户在参观前做好充分的准备，也有助于提升用户的参观体验，使得用户能够更加深刻地理解和感受红色文化的独特魅力。
此外，系统还具备添加景点的功能，这使得用户和管理人员能够不断地丰富和更新系统内的景点信息。用户可以通过简单的操作，将自己的发现或者新的红色文化景点信息添加到系统中，这样不仅为系统带来了更多的内容，也使得系统能够持续地发展和完善。
总的来说，上海市红色文化景点导览系统是一款集地图导航、文化教育和信息共享于一体的综合性应用程序。它的推出，不仅为用户提供了一个便捷的方式来了解和参观上海市的红色文化景点，也为红色文化的传播和教育提供了一个有效的平台。能够对提升公众的历史意识和文化素养发挥作用。
''')
    st.info("由于公有云的限制，若一段时间无人访问，网站会关闭，在此设立管理员入口，方便通过直接载入配置文件来快速恢复网站。请勿擅动，谢谢！")
    a=st.text_input("请输入管理员密码：")
    if a=="OpenControl":
        def list_files(directory):
            files = os.listdir(directory)
            a = pd.DataFrame(columns=['s'])
            for file in files:
                if os.path.isfile(os.path.join(directory, file)):
                    a = a._append(
                        {"s": file}, ignore_index=True)
            return a


        k = list_files('./')
        try:
            s = st.selectbox("请选择要下载的内容",
                             k['s'])
            file1 = open(s, 'rb')
            st.download_button(
                label="Download data",
                data=file1,
                file_name=s,
                mime='text',
            )
            file1 = st.file_uploader("上传文件")
            bytes_data = file1.read()
            with open(file1.name, "wb") as file:
                file.write(bytes_data)
            st.success("上传成功！")
        except AttributeError:
            pass
    elif a != '':
        st.error("密码错误！")




