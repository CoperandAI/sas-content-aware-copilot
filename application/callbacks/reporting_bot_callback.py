import dash
from dash import Input, Output, State
import dash_bootstrap_components as dbc
from application.functions.reporting_bot_functions import format_response
from application.models.chat_model import memory
from application.models.chat_model import retriever, gpt4o
from langchain.schema import AIMessage
import re
import markdown
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML

def register_reporting_bot_callback(app):
    """Registers the chatbot-related callbacks with the Dash app."""
    
    @app.callback(
        Output("chat-output", "children"),
        Input("send-button", "n_clicks"),
        State("user-input", "value"),
        prevent_initial_call=True
    )
    def chatbot_response(n_clicks, user_input):
        if user_input:
            search_results = retriever.get_relevant_documents(user_input)
            context = "\n".join([doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc in search_results])
            response = gpt4o.invoke(f"Context: {context}\nUser: {user_input}")

            memory.save_context({"input": user_input}, {"output": response.content})
            chat_history = list(reversed(memory.load_memory_variables({})["chat_history"]))

            chat_elements = []
            for msg in chat_history:
                chat_elements.append(
                    dbc.Card(
                        dbc.CardBody(format_response(msg.content)),  # ✅ Use the new function
                        color="#f0f0f0" if isinstance(msg, AIMessage) else "#673ab7",
                        inverse=not isinstance(msg, AIMessage),
                        style={"max-width": "90%", "margin-bottom": "5px"}
                    )
                )
            return chat_elements

        return ""
