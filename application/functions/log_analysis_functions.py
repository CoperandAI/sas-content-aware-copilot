import re
from application.models.chat_model import gpt4o, retriever, memory

def retrieve_metadata_context(user_input):
    try:
        docs = retriever.invoke(user_input)
        if not docs:
            return "No relevant metadata found."
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"❌ Metadata retrieval failed: {e}")
        return "No relevant metadata found."

# ✅ Analyze SAS Log


def analyze_log(log_file):
    warnings, errors = 0, 0
    error_messages, warning_messages = [], []
    try:
        with open(log_file, "r", encoding="utf-8") as file:
            log_text = file.read()
            error_matches = re.findall(
                r"ERROR:.*?(?=\n\S|$)", log_text, re.DOTALL)
            warning_matches = re.findall(
                r"WARNING:.*?(?=\n\S|$)", log_text, re.DOTALL)
            errors, warnings = len(error_matches), len(warning_matches)
            error_messages, warning_messages = error_matches, warning_matches
    except Exception as e:
        print(f"❌ Error processing {log_file}: {e}")
    return warnings, errors, error_messages, warning_messages

# ✅ Get LLM Analysis (Only First Warning & First Error)


def get_llm_analysis(log_file, error_messages, warning_messages):
    results = []
    try:
        with open(log_file, "r", encoding="utf-8") as file:
            full_log_content = file.read()
    except Exception as e:
        print(f"❌ Error reading log file {log_file}: {e}")
        return []

    first_error = error_messages[0] if error_messages else None
    first_warning = warning_messages[0] if warning_messages else None
    issues_to_analyze = []

    if first_error:
        issues_to_analyze.append(("ERROR", first_error))
    if first_warning:
        issues_to_analyze.append(("WARNING", first_warning))

    metadata_context = retrieve_metadata_context("Analyze SAS logs")

    for issue_type, message in issues_to_analyze:
        full_prompt = (
            f"SAS runs sequentially, meaning errors in early steps often cause failures in later steps. "
            f"Focus **only on the first error and first warning**.\n\n"
            f"### Metadata Context\n{metadata_context}\n\n"
            f"### SAS Log Issue\n"
            f"- **Issue Type:** {issue_type}\n"
            f"- **Log Message:**\n{message}\n\n"
            f"### Output Format:\n"
            f"- **Analysis**: One short sentence explaining the issue.\n"
            f"- **Resolution**: One or two sentences suggesting a fix."
        )

        try:
            response = gpt4o.invoke(full_prompt)
            explanation, resolution = response.content.split(
                "\n", 1) if "\n" in response.content else (response.content, "No resolution suggested")
            results.append(
                (issue_type, explanation.strip(), resolution.strip()))
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            continue

    return results
