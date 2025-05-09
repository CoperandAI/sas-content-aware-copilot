import dash_bootstrap_components as dbc
from dash import html

def navbar_ui():
    return dbc.Navbar(
        dbc.Container(fluid=True, children=[
            # ✅ Add Logo
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="/assets/coperand_logo.png", height="40px")),
                ], align="center", className="g-0"),
                href="/",
                style={"textDecoration": "none"}  # Removes underline effect
            ),

            # ✅ Navigation Links
            dbc.Row([
                dbc.Col(dbc.NavItem(dbc.NavLink(
                    "Ask Your Data", href="/reporting-bot", style={"color": "white"})), width="auto"),
                dbc.Col(dbc.DropdownMenu(
                    label="Report Validator", nav=True, in_navbar=True, style={"color": "white"}, children=[
                        dbc.DropdownMenuItem(
                            "Run Validator", href="/run-validator"),
                        dbc.DropdownMenuItem(
                            "Validation History", href="/validation-history")
                    ]), width="auto"
                ),
                dbc.Col(dbc.DropdownMenu(
                    label="Log Analytics", nav=True, in_navbar=True, style={"color": "white"}, children=[
                        dbc.DropdownMenuItem(
                            "Run Log Analytics", href="/log-analytics"),
                        dbc.DropdownMenuItem(
                            "History", href="/log-analytics-history")
                    ]), width="auto"
                ),
                dbc.Col(dbc.NavItem(dbc.NavLink(
                    "Automation", href="/automation", style={"color": "white"})), width="auto"),
                dbc.Col(dbc.NavItem(dbc.NavLink("Help", href="/help",
                        style={"color": "white"})), width="auto")
            ], align="center", className="ms-3", justify="start")
        ]),
        color="#673ab7", dark=True, className="mb-4", style={"position": "fixed", "width": "100%", "z-index": "1000", "top": "0"}
    )
