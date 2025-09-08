from langchain.agents import Tool
import webbrowser
from pywhatkit import playonyt
# from AppOpener import open, close
from datetime import datetime
import dearpygui.dearpygui as dpg
import subprocess
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
    print("------------- Date function called")
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


def show_popup(title, message):
    """Shows a desktop notification popup.
    Args:
        title (str): The title of the popup.
        message (str): The message content of the popup.
    Returns:
        str: Confirmation message."""
    command = [
        "terminal-notifier",
        "-title", title,
        "-message", message,
        "-sound", "default"
    
    ]

    subprocess.run(command)
    return f"Displayed popup with title: {title}"


def write_file(filename: str, content: str):
    """Writes content to a file (overwrites existing content).
        Args:
            filename (str): The name of the file.
            content (str): The content to write to the file.
        Returns:
            str: Confirmation message."""
    try:
        with open(f"/Users/ravisharma/PycharmProjects/Advance_jarvis/{filename}", 'w') as file:
            file.write(content)
        return f"Wrote content to {filename}."
    except Exception as e:
        return f"Error: {e}"

def append_file(filename: str, content: str):
    """Appends content to the end of a file.
        Args:
            filename (str): The name of the file.
            content (str): The content to append to the file.
        Returns:
            str: Confirmation message."""
    try:
        with open(f"/Users/ravisharma/PycharmProjects/Advance_jarvis/{filename}", 'a') as file:
            file.write(content)
        return f"Appended content to {filename}."
    except Exception as e:
        return f"Error: {e}"

def read_file(filename: str):
    """Reads content from a file.
        Args:
            filename (str): The name of the file.
        Returns:
            str: The content of the file or error message."""
    try:
        with open(f"/Users/ravisharma/PycharmProjects/Advance_jarvis/{filename}", 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error: {e}"


def get_user_input(CONTENT):
    """Displays a popup window to get user input.
    Args:
        CONTENT (str): The message to display in the popup.
    Returns:        str: The user input from the popup."""
    result = {"text": None}

    def submit_callback(sender, app_data, user_data):
        result["text"] = dpg.get_value("input_field")
        dpg.stop_dearpygui()

    dpg.create_context()

    # --- Global styling ---
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 25, 240))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (45, 135, 245, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (75, 155, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (35, 115, 215, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40, 220))
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 6)

    # --- Popup Window ---
    with dpg.window(label="Jarvis Assistant", tag="popup_window",
                    width=420, height=180, no_resize=True,
                    no_collapse=True, no_move=True, no_close=True):
        dpg.add_text(CONTENT, color=(200, 200, 200))
        dpg.add_spacer(height=8)
        dpg.add_input_text(tag="input_field", hint="Write here...",
                           on_enter=True, callback=submit_callback,
                           width=380)
        dpg.add_spacer(height=6)
        dpg.add_button(label="ENTER", callback=submit_callback, width=100)

    dpg.bind_theme(global_theme)

    # --- Center popup on screen ---
    dpg.create_viewport(title='Jarvis Input', width=420, height=180, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    vp_w, vp_h = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    screen_w, screen_h = dpg.get_viewport_width(), dpg.get_viewport_height()
    dpg.set_viewport_pos(((screen_w - vp_w)//2, (screen_h - vp_h)//2))

    dpg.start_dearpygui()
    dpg.destroy_context()

    return result["text"]