from fastmcp import FastMCP
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from utils import Classification, get_posts_n_messages, query_prompt, reddit

mcp = FastMCP("social_media")


@tool
def reddit_tool(query: str) -> str:
    """Use this tool to query messages from social media."""
    subs = ["StockMarket", "investing", "wallstreetbets"]

    serialized = ""
    all_comments = []
    for sub in subs:
        subreddit = reddit.subreddit(sub)
        comments = get_posts_n_messages(query, subreddit)
        all_comments.append(comments)

    serialized = "\n\n".join((f"{comment}") for comment in all_comments)
    return serialized


@mcp.tool
def get_social_sentiment(
    ticker: str,
    company: str,
    model: str,
) -> dict:
    llm_social = ChatOllama(
        model=model,
        temperature=0.2,
    )
    agent_executor = create_react_agent(llm_social, [reddit_tool])

    structured_output = ChatOllama(
        model=model,
        temperature=0.2,
    ).with_structured_output(Classification)

    msg = query_prompt.invoke({"query": [f"{ticker} OR {company}"]})
    response = agent_executor.invoke(msg)
    return structured_output.invoke(
        response["messages"][-1].content.split("</think>")[-1],
    )  # type: ignore


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=9002)
