import streamlit as st
import pandas as pd

from analysis.statistics import Statistics
from analysis.optimizer import Optimizer

def show_sidebar():
    with st.sidebar:
        budget = st.number_input(
            "購入予定数",
            min_value=1,
            value=10
        )
        
        threshold = st.slider(
            "当たり判定",
            min_value=1,
            max_value=10,
            value=8
        )
    
    return budget, threshold

def show_input():
    groups = st.session_state.groups
    for group in groups:
        count = sum(item.score == 0 for item in group.items)
        title = group.name
        if count > 0:
            title += f"(未入力){count}人"
        with st.expander(title):
            with st.container(height=450):
                for item in group.items:
                    key=f"{group.name}_{item.name}"
                    if key not in st.session_state:
                        st.session_state[key] = 0
                    
                    item.score = st.selectbox(
                        label=item.name,
                        options=list(range(0, 11)),
                        key=key,
                    )

def show_statistics(groups, threshold):
    st.header("分析結果")
    
    for group in groups:
        scores = Statistics.scores(group)
        mean = Statistics.mean(scores)
        var = Statistics.var(scores)
        hit = Statistics.hit_rate(scores, threshold)

        st.subheader(group.name)

        c1, c2, c3 = st.columns(3)

        c1.metric("平均", f"{mean:.2f}")
        c2.metric("分散", f"{var:.2f}")
        c3.metric("当たり率", f"{hit:.1%}")

def show_recommendation(groups, budget, threshold):
    recommendation = Optimizer.recommend(groups, budget)
    
    rows = []
    
    for group, count in recommendation.items():
        scores = Statistics.scores(group)
        rows.append({
            "グループ": [group.name],
            "平均": [f"{Statistics.mean(scores):.2f}"],
            "分散": [f"{Statistics.var(scores):.2f}"],
            "当たり率": [f"{Statistics.hit_rate(scores, threshold):.1%}"],
            "おすすめ購入数": [count]
        })
    
    df = pd.DataFrame(rows)

    st.header("おすすめ購入数")
    
    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )
        