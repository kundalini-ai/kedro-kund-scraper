"""
This is a boilerplate pipeline 'journal_finetuning_db_pipeline'
generated using Kedro 0.19.6
"""
import pandas as pd
from clearpilldatabase.utils import generate_finetuning_data

def finetuning_db_node(articles_content : pd.DataFrame):
    finetuning_data = []
    instruction = "What market trend does this article represent?"
    for article in articles_content:
        result = generate_finetuning_data(instruction, article['content'])
        finetuning_data.append(result)
    return finetuning_data
