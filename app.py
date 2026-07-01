import streamlit as st
import pandas as pd
from dataio.loader import load_all_groups, load_template
from analysis.statistics import Statistics
from analysis.optimizer import Optimizer

from ui import (
    show_sidebar,
    show_statistics,
    show_recommendation
)

st.set_page_config(
    page_title="ランダム購入支援ツール",
    layout="wide"
)

st.title("ランダム購入支援ツール")

groups = load_template("templates/real_capsule_toy.json")
budget, threshold = show_sidebar()
for group in groups:
    with st.expander(group.name):
        with st.container(height=450):
            col1, col2 = st.columns([4, 1])
            for item in group.items:
                with col1:
                    st.write(item.name)
                with col2:
                    item.score = st.selectbox(
                        "",
                        list(range(1, 11)),
                        index=item.score - 1,
                        key=f"{group.name}_{item.name}",
                        label_visibility="collapsed"
                    )

if st.button("おすすめを計算"):
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