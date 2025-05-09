import re
import markdown
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML

def format_response(response_text):
    """Formats bot responses to correctly render Markdown, lists, and code blocks."""
    response_text = response_text.strip()

    # Fix incorrectly formatted numbered lists (Ensure proper Markdown list syntax)
    response_text = re.sub(r"(\d+)\.\s", r"\n\1. ", response_text)  # Add newlines before numbered lists
    response_text = re.sub(r"-\s", r"\n- ", response_text)  # Add newlines before bullet points

    # Convert Markdown to HTML (handles bullet points, numbered lists, code blocks, etc.)
    response_html = markdown.markdown(response_text, extensions=["fenced_code", "tables"])

    return DangerouslySetInnerHTML(response_html)
