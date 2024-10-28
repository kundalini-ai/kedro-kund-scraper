"""
This is a boilerplate pipeline 'journal_scrape_pipeline'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import scrape_articles_node

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=scrape_articles_node,
            inputs='bsa_fetched_articles',
            outputs='bsa_articles_content',
            name="journal_scrape_node"
        ),
    ],
        inputs={"bsa_fetched_articles": "bsa_fetched_articles"},
        outputs="bsa_articles_content",
        namespace="bsa_scrape",
    )
