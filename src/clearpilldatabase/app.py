from typing import List

from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

from kedro_boot.app.fastapi.session import KedroFastApi

app = FastAPI(title="Database generation")

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")

class Topics(BaseModel):
    topic: str = "Halving"

class FetchedArticles(BaseModel):
    articles: List

class ArticlesContent(BaseModel):
    articles: List

@app.post('/fetch_articles', operation_id="journal_data")
def fetched_articles(
        topics: Topics, kedro_run: KedroFastApi
) -> FetchedArticles:
    # run_params = {"topics": topics.dict()}
    # result = kedro_run.run(pipeline_name="journal", run_params=run_params)
    return {
        "articles": kedro_run
    }

@app.post('/articles_content', operation_id="journal_scrape")
def articles_content(
        fetched_articles: FetchedArticles, kedro_run: KedroFastApi
) -> ArticlesContent:
    return {
        "articles": kedro_run
    }