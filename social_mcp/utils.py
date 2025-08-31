import os

import praw
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from praw.reddit import Subreddit
from pydantic import BaseModel, Field


class Classification(BaseModel):
    """template"""

    query: str = Field(description="Add here exatcly the text from the 'query' field")
    sentiment: float = Field(description="Add here exatcly what is written in the Sentiment part of the message")
    summary: str = Field(description="Add here exatcly what is written in the Summary part of the message")


query_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a social media expert and analyst. Call the tool once using the '_query_' \
            below exactly as the user provided. Do NOT modify it! \
            You HAVE TO call the reddit_tool once and ONLY once. \
            Extract social media messages from the Tool reply. \
            Analyze the messages as they are. You must be neutral. \
            --- \
            **IMPORTANT**: If no reply from the Tool, DO NOT INVENT any information. \
            Just write 'empty' for Summary. \
            --- \
            _query_ = {query} \
            Only extract Sentiment and perform a Summary, following the structure below and do \
            not add anything extra in your message: \
            -Query: Add here the query you used when calling the tool \
            -Sentiment: The sentiment of the messages in a scale from 0.0 (negative) to 5.0 (positive). \
            -Summary: A detailed summary representing the overall comments.",
        ),
        MessagesPlaceholder(variable_name="query"),
    ],
)


reddit = praw.Reddit(
    client_id=os.getenv("REDT_ID"),
    client_secret=os.getenv("REDT_PASS"),
    user_agent="Comment Extraction/fincrw",
)

reddit.read_only = True


def get_posts_n_messages(
    query: str,
    subreddit: Subreddit,
    search_limit: int = 5,
    max_comments: int = 10,
) -> str:
    submission = None
    for submission in subreddit.search(
        query,
        sort="relevance",
        time_filter="month",
        limit=search_limit,
    ):
        # Limit, sort and Load comments
        submission.comment_sort = "top"
        submission.comment_limit = max_comments
        # Remove "load more comments" prompts
        submission.comments.replace_more(limit=0)

    if submission:
        serialized = "\n\n".join(
            (f"{comment.body}")  # type: ignore
            for comment in submission.comments.list()  # type: ignore
        )
        return serialized
    # if the search returns nothing
    return ""
