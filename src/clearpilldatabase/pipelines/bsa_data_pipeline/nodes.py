"""
This is a boilerplate pipeline 'journal_data_pipeline'
generated using Kedro 0.19.6
"""
from typing import Dict
from clearpilldatabase.utils import search_articles
import pandas as pd

def search_articles_node(topics: pd.DataFrame, journals: pd.DataFrame, results_number):
    articles = search_articles(topics, journals, results_number)
    return articles
