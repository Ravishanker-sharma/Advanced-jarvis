from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("GEMINI_API_KEY")
mcp_server_url = os.getenv("MCP_SERVER_URL")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key = api,
    temperature=0.7,
model_kwargs={"streaming": True}
)

