import re

# Function to clean Analysis & Resolution text
def clean_markdown_text(text):
    # Removes "Analysis" & "Resolution"
    return re.sub(r"- \*\*(Analysis|Resolution)\*\*: ?", "", text)