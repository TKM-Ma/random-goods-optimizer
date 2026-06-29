import streamlit as st

from dataio.loader import load_all_groups
from analysis.optimizer import Optimizer

def main():
    groups = load_all_groups("data/score_data.xlsx")
    
    for i in groups:
        i.print_status()
    
    for i, j in Optimizer.recommend(groups, 50).items():
        print(i.name)
        print(j)
    
if __name__ == "__main__":
    main()