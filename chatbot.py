from langgraph.graph import StateGraph, add_messages
from typing import Annotated, TypedDict
from langgraph.prebuilt import tools_condition, ToolNode
from scraper import get_data
from langchain.agents import Tool
from langgraph.checkpoint.memory import MemorySaver
from config import llm
from tools import open_website, play_youtube_video, get_current_date, execute_system_command

memory = MemorySaver()

class Agent_state(TypedDict):
    messages: Annotated[list, add_messages]

tools = [
    Tool(
        name="GetData",
        func=get_data,
        description="Performs a websearch on basis of input and return data."
    ),
    Tool(
        name="OpenWebsite",
        func=open_website,
        description="Opens a website in the default web browser. Input should be a valid URL starting with http or https."
    ),
    Tool(
        name="PlayYouTubeVideo",
        func=play_youtube_video,
        description="Plays a YouTube video based on the search query. Input should be the name or keywords of the video to be played."
    ),
    Tool(
        name="GetCurrentDate",
        func=get_current_date,
        description="Gets the current system date and time. Input should be keyword = time."
    ),
    Tool(
        name="ExecuteSystemCommand",
        func=execute_system_command,
        description="Executes a system command. Input should be a valid system command as a string."
    )
]

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


intialized_threads = set()

def jarvis(message,thread_id="1"):
    if thread_id not in intialized_threads:
        
        prompt = '''
        You are a Jarvis Desktop Assistant Developed by CODEX.
        If you think some task can be better accomplished by using a tool, you must use the appropriate tool.
        if you think  you dont have a tool to do a task but , you can do it by executing a system command, you must use the tool named "ExecuteSystemCommand".
        '''
        msg = {"messages": [{"role":"system","content":prompt},{"role": "user", "content": message}]}
        intialized_threads.add(thread_id)
    else:
        msg = {"messages": [{"role": "user", "content": message}]}
    config1 = {"configurable": {"thread_id":thread_id}}
    output = app.invoke(msg, config=config1)
    return output['messages'][-1].content

def clear_threads(thread_id):
    global intialized_threads
    if thread_id not in intialized_threads:
        intialized_threads.clear()


def chat(message):
    clear_threads("1")
    return jarvis(message)



if __name__ == '__main__':
    print(chat("open google.com"))