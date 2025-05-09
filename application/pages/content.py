from dash import html

def content_ui():
    return html.Div(id="page-content", style={
        "margin-left": "270px",
        "margin-top": "60px",
        "padding": "20px",
        "background": "white",
        "min-height": "100vh",
        "overflow-y": "auto"
    })
