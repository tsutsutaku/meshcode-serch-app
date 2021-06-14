import streamlit as st
from streamlit_folium import folium_static
import folium
import jismesh.utils as ju
import requests

API_KEY = st.secrets["API_KEY"]
PASSWORD = st.secrets["PASSWORD"]

def get_grid_position(lat, lon, level):
    meshcode = ju.to_meshcode(lat, lon, level)
    lat_sw, lon_sw = ju.to_meshpoint(meshcode, 0, 0)
    lat_se, lon_se = ju.to_meshpoint(meshcode, 0, 1)
    lat_nw, lon_nw = ju.to_meshpoint(meshcode, 1, 0)
    lat_ne, lon_ne = ju.to_meshpoint(meshcode, 1, 1)
    sq = [(lat_sw, lon_sw), (lat_se, lon_se), (lat_ne, lon_ne), (lat_nw, lon_nw)]

    return  sq

st.title("メッシュコード検索アプリ")

st.markdown("### 緯度経度やランドマーク名からメッシュコードを算出します。")

st.write("")
st.write("")
st.write("")
st.write("")


selected_item = st.selectbox('入力する項目を選択してください。',
                                 ['緯度経度', 'ランドマーク名'])

st.write("")
st.write("")

if selected_item == "緯度経度":
    st.write("緯度経度を入力してください。")
    col1, col2= st.beta_columns(2)
    with col1:
        lat = st.number_input(label='latitude', value=35.6809591, format="%3g")
    with col2:
        lon = st.number_input(label='longitude', value=139.7673068, format="%3g")
    
    
    level = st.selectbox("メッシュレベルを入力してください",
                                 [1,2,3,4,5])
    
    
    #lat, lon = 35.7100069 , 139.8108103
    meshcode = ju.to_meshcode(lat, lon, level)
    st.write(f"{level}次メッシュコード: {meshcode}")
    lat_c, lon_c = ju.to_meshpoint(meshcode, 0.5, 0.5)

    if level == 1:
        m = folium.Map(location=[lat_c, lon_c], zoom_start=8)
    
    elif level == 2:
        m = folium.Map(location=[lat_c, lon_c], zoom_start=11)
    
    elif level == 3:
        m = folium.Map(location=[lat_c, lon_c], zoom_start=14)
    
    elif level == 4:
        m = folium.Map(location=[lat_c, lon_c], zoom_start=15)
    
    elif level == 5:
        m = folium.Map(location=[lat_c, lon_c], zoom_start=16)

    sq = get_grid_position(lat, lon, level)

    folium.Polygon(
        locations=sq, # 多角形の頂点
        color="red", # 線の色
        weight=3, # 線の太さ
        fill=True, # 塗りつぶす
        fill_opacity=0.5 # 透明度（1=不透明）
    ).add_to(m)

    message=str(meshcode)

    folium.Marker([lat, lon]).add_to(m)

    #folium.Marker(location=[lat, lon], popup=message).add_to(m)

    folium_static(m)

else:
    input_password = st.text_input(label="パスワードを入力してください", value='', type="password")

    name = ""
    
    if input_password == PASSWORD:
        name = st.text_input(label="ランドマーク名を入力してください", value='')

    m = folium.Map(location=[35.7100069 , 139.8108103], zoom_start=8)

    #folium_static(m)
    
    if name != "":
        req = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={name}&key={API_KEY}")
        req_json = req.json()

        lat = req_json['results'][0]['geometry']['location']['lat']
        lon = req_json['results'][0]['geometry']['location']['lng']

        st.write(f"{name}　緯度:{lat}　　 経度:{lon}")

        level = st.selectbox("メッシュレベルを入力してください",
                                 [1,2,3,4,5])
    
    
        meshcode = ju.to_meshcode(lat, lon, level)
        st.write(f"{level}次メッシュコード: {meshcode}")
        lat_c, lon_c = ju.to_meshpoint(meshcode, 0.5, 0.5)

        if level == 1:
            m = folium.Map(location=[lat_c, lon_c], zoom_start=8)

        elif level == 2:
            m = folium.Map(location=[lat_c, lon_c], zoom_start=11)

        elif level == 3:
            m = folium.Map(location=[lat_c, lon_c], zoom_start=14)

        elif level == 4:
            m = folium.Map(location=[lat_c, lon_c], zoom_start=15)

        elif level == 5:
            m = folium.Map(location=[lat_c, lon_c], zoom_start=16)

        sq = get_grid_position(lat, lon, level)

        folium.Polygon(
            locations=sq, # 多角形の頂点
            color="red", # 線の色
            weight=3, # 線の太さ
            fill=True, # 塗りつぶす
            fill_opacity=0.5 # 透明度（1=不透明）
        ).add_to(m)

        folium.Marker([lat, lon]).add_to(m)


    #folium.Marker(location=[lat, lon], popup=message).add_to(m)

    folium_static(m)



