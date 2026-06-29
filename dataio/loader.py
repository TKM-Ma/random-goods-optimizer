import csv
import pandas as pd

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