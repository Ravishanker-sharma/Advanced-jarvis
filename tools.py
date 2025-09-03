from langchain.agents import Tool
import webbrowser
from pywhatkit import playonyt
# from AppOpener import open, close
from datetime import datetime
import os

def open_website(url: str):
    """Opens a website in the default web browser.
        Args:
            url (str): The URL of the website to open.
        Returns:
            str: Confirmation message."""
    webbrowser.open(url)
    return f"Opened {url} in your web browser."


def play_youtube_video(query: str):
    """Plays a YouTube video based on the search query.
        Args:
            query (str): The search query for the YouTube video.
        Returns:
            str: Confirmation message."""
    playonyt(query)
    return f"Playing {query} on YouTube."

# def open_application(app_name: str):
#     """Opens a desktop application.
#         Args:
#             app_name (str): The name of the application to open.
#         Returns:
#             str: Confirmation message."""
#     open(app_name)
#     return f"Opened {app_name} application."

# def close_application(app_name: str):
#     """Closes a desktop application.
#         Args:
#             app_name (str): The name of the application to close.
#         Returns:
#             str: Confirmation message."""
#     close(app_name)
#     return f"Closed {app_name} application."


def get_current_date(x:str):
    """Gets the current system date and time.
        Args:
            x (str): keyword = time
        Returns:
            str: The current date and time in YYYY-MM-DD HH:MM format."""
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M")
    return f"The current date and time is {current_date_time}."

def execute_system_command(command: str):
    """Executes a system command.
        Args:
            command (str): The system command to execute.
        Returns:
            str: Confirmation message."""
    os.system(command)
    return f"Executed command: {command}"

