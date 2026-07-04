import json
import pandas as pd

import streamlit as st

from models.item import Item
from models.group import Group

def load_all_groups(file):
    groups = []
    excel = pd.ExcelFile(file)
    
    for sheet in excel.sheet_names:
        groups.append(load_group(excel, sheet))
    
    return groups

def load_group(excel, sheet):
    items = []
    
    df = pd.read_excel(excel, sheet_name=sheet)
    for _, row in df.iterrows():
        items.append(Item(row["name"], row["score"]))
    
    return Group(sheet, items)

def load_template(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    groups = []
    for group_data in data["groups"]:
        items = []
        
        for name in group_data["items"]:
            items.append(Item(name, 0))
        
        groups.append(
            Group(
                group_data["name"],
                items
            )
        )
    return groups

def apply_score(upload_file):
    groups = st.session_state.groups
    score_data = json.load(upload_file)
    
    for group in groups:
        if group.name not in score_data:
            continue
        
        for item in group.items:
            if item.name in score_data[group.name]:
                item.score = score_data[group.name][item.name]

                st.session_state[f"{group.name}_{item.name}"] = item.score