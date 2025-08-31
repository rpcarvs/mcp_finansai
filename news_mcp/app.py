from fastmcp import FastMCP
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from utils import Classification, query_prompt, tav_search

mcp = FastMCP("financial_news")


@mcp.tool
def get_financial_news(ticker: str, company: str, model: str) -> dict:
    llm_financial = ChatOllama(
        model=model,
        temperature=0.2,
    )
    agent_executor = create_react_agent(llm_financial, [tav_search])

    structured_output = ChatOllama(
        model=model,
        temperature=0.2,
    ).with_structured_output(Classification)

    msg = query_prompt.invoke(
        {
            "query": [
                f"What are the most relevant financial news about {ticker} or {company}?",
            ],
        },
    )
    response = agent_executor.invoke(msg)
    return structured_output.invoke(
        response["messages"][-1].content.split("</think>")[-1],
    )  # type: ignore


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=9001)
