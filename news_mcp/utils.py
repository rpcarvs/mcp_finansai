from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily.tavily_search import TavilySearch
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
            "You are a financial news and stock market expert. Call the tool once using the '_query_' \
            below exactly as the user provided. Do NOT modify it! \
            You HAVE TO call the tav_search tool once and ONLY once. \
            _query_ = {query} \
            Extract information from the Tool reply. \
            Analyze the information as it is. You must be neutral. \
            --- \
            **IMPORTANT**: If no reply from the Tool, DO NOT INVENT any information. \
            Just write 'empty' for Summary. \
            --- \
            Only extract Sentiment and perform a Summary, following the structure below and do \
            not add anything extra in your message: \
            -Query: Add here the query you used when calling the tool \
            -Sentiment: The sentiment of the messages in a scale from 0.0 (negative) to 5.0 (positive). \
            -Summary: A detailed and long summary representing the retrieved information.",
        ),
        MessagesPlaceholder(variable_name="query"),
    ],
)

tav_search = TavilySearch(
    max_results=5,
    days=30,
    topic="news",
    include_answer="advanced",
    search_depth="advanced",
)
