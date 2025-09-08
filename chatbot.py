import asyncio
from langgraph.graph import StateGraph, add_messages
from typing import Annotated, TypedDict
from langgraph.prebuilt import tools_condition, ToolNode
from scraper import get_data
from langchain.agents import Tool
from langgraph.checkpoint.memory import MemorySaver
from config import llm,mcp_server_url
from tools import open_website, play_youtube_video, get_current_date, execute_system_command , show_popup, write_file, read_file, append_file ,get_user_input
from langchain_mcp_adapters.client import MultiServerMCPClient


client = MultiServerMCPClient({
    "Genral": {
        "url": mcp_server_url,
        "transport": "streamable_http",
    }
})

memory = MemorySaver()

class Agent_state(TypedDict):
    messages: Annotated[list, add_messages]


async def build_app():
    # Local tools
    tools = [
        Tool(
            name="GetData",
            func=get_data,
            description="Performs a websearch on basis of input and return data."
        ),
        Tool(
            name="OpenWebsite",
            func=open_website,
            description="Opens a website in the default web browser."
        ),
        Tool(
            name="PlayYouTubeVideo",
            func=play_youtube_video,
            description="Plays a YouTube video based on the search query."
        ),
        Tool(
            name="GetCurrentDate",
            func=get_current_date,
            description="Gets the current system date and time."
        ),
        Tool(
            name="ExecuteSystemCommand",
            func=execute_system_command,
            description="Executes a system command. Input should be a valid system command as a string."
        ),
        Tool(
            name="ShowPopup",
            func=show_popup,
            description="Shows a desktop notification popup with a title and message. Input should be in the format 'title | message'."
        ),
        Tool(
            name="WriteFile",
            func=write_file,
            description="Writes content to a file. Input should be in the format 'filename | content'."
        ),
        Tool(
            name="ReadFile",
            func=read_file,
            description="Reads content from a file. Input should be the filename as a string."
        ),
        Tool(
            name="AppendFile",
            func=append_file,
            description="Appends content to a file. Input should be in the format 'filename | content'."
        ),
        Tool(
            name="GetUserInput",
            func=get_user_input,
            description="Displays a popup window to get user input. Input should be the message to display in the popup."
        )
    ]

    # ✅ Add MCP tools dynamically
    mcp_tools = await client.get_tools()
    tools.extend(mcp_tools)

    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)

    def chat_bot(state: Agent_state):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph = StateGraph(Agent_state)
    graph.add_node("bot", chat_bot)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("bot")
    graph.add_conditional_edges("bot", tools_condition)
    graph.add_edge("tools", "bot")

    app = graph.compile(checkpointer=memory)
    return app
intialized_threads = set()

async def jarvis(app, message, thread_id="1"):
    if thread_id not in intialized_threads:
        prompt = '''
        You are a Jarvis Desktop Voice Assistant Developed by CODEX.
        If you think some task can be better accomplished by using a tool, you must use the appropriate tool.
        If you don’t have a tool to do a task but you can do it by executing a system command, you must use the tool named "ExecuteSystemCommand".
        Keep your replies concise , to the point and minimal , keep it under 50 words. (If word limit exceeds use tool to save information in a file and tell user that you have saved that information to a file with filename).
        As you are voice assistant do not use any special characters in your response or something which is not easy to speak out loud.
        Use the tool named "ShowPopup" to show any kind of notification or popup on the desktop.
        If something is too big for sepaking out loud for example a code or a essay , you can use the tool to write that information to a file and tell the user that you have saved that information to a file with filename.
        If you do not have tools for something such as genrating a code or essay , you can do it by yourself (You are a AI).
        You can use the tool named "GetUserInput" to get input from user in form of a popup window. You should use this tool when , something is difficult to be detected in speech to text form such as email ids , passwords , specific names or places.
        Always reconfirm email ids or passwords by spelling them out chracter by character. ( If user says it is wrong , use GetUserInput tool to get the correct email id or password).
        '''
        msg = {"messages": [{"role": "system", "content": prompt},
                            {"role": "user", "content": message}]}
        intialized_threads.add(thread_id)
    else:
        msg = {"messages": [{"role": "user", "content": message}]}

    config1 = {"configurable": {"thread_id": thread_id}}
    output = await app.ainvoke(msg, config=config1)
    return output['messages'][-1].content


async def main():
    app = await build_app()
    response = await jarvis(app, "get me details about my calander , use my primary id only ")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
