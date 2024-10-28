import os

from langchain_community.utilities import GoogleSerperAPIWrapper
import openai

openai_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(
  api_key=openai_key
)


graph_config = {
   "llm": {
      "api_key": openai_key,
      "model": "gpt-4-turbo",
   },
}


def search_articles(topics, journals, results_number):
    google_serper = GoogleSerperAPIWrapper(k=results_number)
    articles = []

    for journal in journals:
        for topic in topics:
            query = f'{topic} site:{journal}'
            result = google_serper.results(query)

            for result in result['organic']:
                articles.append({
                    "title": result['title'],
                    "link": result['link'],
                    "snippet": result['snippet']
                })

    print(len(articles))
    return articles

def get_article_trend(instruction, article):
    response = client.chat.completions.create(
        model='gpt-4-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"{instruction} {article}"}
        ],
    )
    return response.choices[0].message.content


def generate_finetuning_data(instruction, context):
    response = get_article_trend(instruction, context)

    return {
        "instruction": instruction,
        "context": context,
        "response": response,
        "category": "classification"
    }

