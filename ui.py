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
        count = sum(
            st.session_state.get(f"{group.name}_{item.name}", item.score) == 0
            for item in group.items
        )
        if count > 0:
            st.caption(f"⚠ 未入力: {count}人")
        else:
            st.caption("✅ 入力完了")
            
        with st.expander(group.name):
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
        c2.metric("分散（リスク）", f"{var:.2f}")
        c3.metric("当たり率", f"{hit:.1%}")

def show_recommendation(groups, budget, threshold):
    recommendation = Optimizer.recommend(groups, budget)
    
    rows = []
    
    for group, count in recommendation.items():
        scores = Statistics.scores(group)
        rows.append({
            "グループ": [group.name],
            "平均": [f"{Statistics.mean(scores):.2f}"],
            "分散（リスク）": [f"{Statistics.var(scores):.2f}"],
            "当たり率": [f"{Statistics.hit_rate(scores, threshold):.1%}"],
            "おすすめ購入数": [f"{count}個"]
        })
    
    df = pd.DataFrame(rows)

    st.header("おすすめ購入数")
    
    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

def show_description():
    st.subheader("このアプリについて")
    st.write("複数のグループに分かれたランダムグッズの購入計画をサポートするツールです。")
    st.write("どのグループを何個購入すれば、ほしいキャラクターを効率よく狙えるかを入力した評価値をもとに計算します")
    
    st.subheader("使い方")

    st.subheader("➀作品を選択")
    st.write("最初に対象となる作品・商品を選択してください")
    
    st.subheader("➁キャラクターを評価")
    st.write("各キャラクターについて、1~10で評価してください")
    st.write("評価の目安")
    st.write("・10:最推しまたは超当たり。最優先で欲しい  \n・8~9:当たり。できれば欲しい  \n・5～7:普通。当たれば嬉しい  \n・2～4:あまり必要ではない  \n・1:不要  \n・0:未評価")
    
    st.subheader("➂予算・条件を入力")
    st.write("購入予定総個数や当たり率（どこから当たりか）を設定してください")

    st.subheader("➃おすすめを計算")
    st.write("入力内容をもとに、おすすめの購入数を表示します")
    st.subheader("評価データの保存")
    st.write("入力した評価はJSONファイルとして保存できます")
    st.write("次回は保存したファイルを読み込むことで、前回の評価をそのまま利用できます")
    st.subheader("注意事項")
    st.write("・評価が未入力（0）のキャラクターがある場合は計算できません。  \n・このツールは入力した評価をもとに購入案を提案するものであり、実際の抽選結果を保証するものではありません。")