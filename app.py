import streamlit as st
import os

from dataio.loader import load_all_groups, load_template, apply_score
from dataio.saver import groups_to_json

from analysis.statistics import Statistics

from ui import (
    show_sidebar,
    show_input,
    show_statistics,
    show_recommendation,
    show_description,
)

title = "ウマ娘　ランダムグッズ購入数計算ツール"
st.set_page_config(
    page_title=title,
    layout="wide"
)

st.title(title)

show_description()

templates = [
    d for d in os.listdir("templates")
    if os.path.isdir(os.path.join("templates", d))
]

selected = st.selectbox(
    "作品を選択",
    ["選択してください"] + templates
)

if selected != "選択してください":
    if (
        "selected_template" not in st.session_state
        or st.session_state.selected_template != selected
    ):
        path = f"templates/{selected}/template.json"
        st.session_state.groups = load_template(path)
    groups = st.session_state.groups


    uploaded = st.file_uploader(
        "評価ファイル",
        type="json",
    )
    if st.button("ファイルを読み込む"):
        if uploaded is not None:
            apply_score(uploaded)

    show_input()

    budget, threshold = show_sidebar()
    
    json_data = groups_to_json(groups)

    st.download_button(
        "スコアを保存",
        data=json_data,
        file_name="score.json",
        mime="application/json"
    )

    if st.button("おすすめを計算"):
        if Statistics.find_unrated_items(groups):
            st.error("未評価のキャラがあります")
            st.stop()
        show_recommendation(groups, budget, threshold)

    def excel():
        upload_file = st.file_uploader(
            "Exelファイルを選択してください",
            type=["xlsx"]
        )

        if upload_file is not None:
            groups = load_all_groups(upload_file)

            budget, threshold = show_sidebar()
            
            show_statistics(groups, threshold)

            if st.button("おすすめを計算"):
                show_recommendation(groups, budget, threshold)