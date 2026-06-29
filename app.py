import streamlit as st
import pandas as pd
from dataio.loader import load_all_groups
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