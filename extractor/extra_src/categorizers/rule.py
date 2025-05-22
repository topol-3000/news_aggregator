import logging
import json
from openai import OpenAI
from airflow.sdk import Variable

logger = logging.getLogger(__name__)
client = OpenAI(api_key=Variable.get("openai_api_key"))


def enrich_with_tags(articles: list[dict], batch_size: int = 10) -> list[dict]:
    """
    Enriches articles with tags using a batched OpenAI call for improved performance and cost-efficiency.

    Args:
        articles: List of article dictionaries with 'title' and 'summary' keys.
        batch_size: Number of articles to process per OpenAI request.

    Returns:
        List of articles with an added 'tags' key containing 10 relevant tags.
    """
    enriched_articles = []

    for batch_start in range(0, len(articles), batch_size):
        batch = articles[batch_start: batch_start + batch_size]
        prompt = _build_batch_prompt(batch)

        try:
            tags_by_index = _fetch_tags_from_openai(prompt)
        except Exception as e:
            logger.error(f"OpenAI request failed for batch starting at index {batch_start}: {e}")
            tags_by_index = {}

        # Map tags back to original articles
        for i, article in enumerate(batch, start=1):
            article["tags"] = tags_by_index.get(i, [])
            enriched_articles.append(article)

    return enriched_articles


def _build_batch_prompt(batch: list[dict]) -> str:
    """
    Creates a structured prompt for OpenAI to return tags for multiple articles.

    Args:
        batch: Subset of articles to include in the prompt.

    Returns:
        A formatted prompt string.
    """
    prompt_lines = [
        "You are a news tagging assistant.",
        "For each article below, return a JSON object with the article index and 5 relevant tags.",
        "Respond only with JSON using this format:",
        '[{"index": 1, "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]}, ...]',
        "Articles:"
    ]

    for i, article in enumerate(batch, start=1):
        title = article.get("title", "").strip()
        summary = article.get("summary", "").strip()
        prompt_lines.append(f'{i}. Title: "{title}"\n   Summary: "{summary}"')

    return "\n\n".join(prompt_lines)


def _fetch_tags_from_openai(prompt: str) -> dict[int, list[str]]:
    """
    Sends the prompt to OpenAI and parses the JSON response into a tag mapping.

    Args:
        prompt: Prompt string with batched article data.

    Returns:
        A dictionary mapping article indexes to lists of tags.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    output_text = response.choices[0].message.content.strip()

    try:
        parsed_output = json.loads(output_text)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse OpenAI response as JSON: {e}\nRaw output:\n{output_text}")
        return {}

    tags_by_index = {
        item["index"]: item["tags"]
        for item in parsed_output
        if isinstance(item, dict) and "index" in item and "tags" in item
    }

    return tags_by_index
