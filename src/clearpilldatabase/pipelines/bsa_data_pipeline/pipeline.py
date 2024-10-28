"""
This is a boilerplate pipeline 'journal_data_pipeline'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import search_articles_node


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=search_articles_node,
            inputs=['topics', 'journals', "results_number"],
            outputs='bsa_fetched_articles',
            name="bsa_data_node"
        ),
    ],
        inputs={"topics": "params:bsa_topics",
                "journals": "params:bsa_journals",
                "results_number": "params:bsa_results_number",
                },
        outputs='bsa_fetched_articles',
        namespace="bsa_data",
    )
