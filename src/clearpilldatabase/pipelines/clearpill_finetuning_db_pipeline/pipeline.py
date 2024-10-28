"""
This is a boilerplate pipeline 'journal_finetuning_db_pipeline'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import finetuning_db_node


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=finetuning_db_node,
            inputs='clearpill_articles_content',
            outputs='clearpill_finetuning_data',
            name="clearpill_finetuning_node"
        ),
    ],
        inputs={"clearpill_articles_content": "clearpill_articles_content"},
        outputs="clearpill_finetuning_data",
        namespace="clearpill_finetuning",
    )

