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
    st.subheader(group.name)

    with st.expander(group.name):
        df = pd.DataFrame({
            "キャラ名":[
                item.name for item in group.items
            ],
            "評価":[
                item.score for item in group.items
            ]
        })
        
        edited = st.data_editor(
            df,
            disabled=["キャラ名"],
            column_config={
                "キャラ名": st.column_config.TextColumn(
                    "キャラ名",
                    width="large",
                ),
                "評価": st.column_config.SelectboxColumn(
                    "評価",
                    options=list(range(1, 11)),
                    width="small",
                    required=True
                )
            },
            hide_index=True
        )
        
    for item, (_, row) in zip(group.items, edited.iterrows()):
        item.score = row["評価"]

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