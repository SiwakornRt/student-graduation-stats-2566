# Import packages
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

# Load data from JSON file
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create DataFrame from JSON data
df = pd.DataFrame(data)

# Convert numerical data from string to integer
df['totalmale'] = df['totalmale'].astype(int)
df['totalfemale'] = df['totalfemale'].astype(int)

# Initialize the Dash app with a dark theme
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

# URL for the Plotly logo
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Define the navigation bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Dashboard", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="dark",
    dark=True,
)

# Define the header section
header = html.Div(children=[
    html.H1(children='Students Graduated Dashboard 2566', style={
            'textAlign': 'center',  # Center text horizontally
            'margin': '20px auto',  # Add margin to center the element horizontally
            'width': '100%'  # Make the H1 take the full width
        }),
    html.P(children='Number of students who graduated from Mathayom 6 in basic education', style={
            'textAlign': 'center',  # Center text horizontally
            'width': '100%'  # Make the paragraph take the full width
        }),
])

# Create options for the province dropdown, including "Select All"
province_options = [{'label': 'Select All', 'value': 'all'}] + [{'label': province, 'value': province} for province in df['schools_province'].unique()]

# Create options for the gender dropdown, including "All"
gender_options = [
    {'label': 'All', 'value': 'all'},
    {'label': 'Male', 'value': 'totalmale'},
    {'label': 'Female', 'value': 'totalfemale'}
]

# Define the filter section with dropdowns for province, gender, and sorting
filter = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H6('Province', style={'margin-bottom': '10px'}),  # Header for the Province dropdown
                        dcc.Dropdown(
                            id='province-dropdown',
                            options=province_options,
                            value=['all'],  # Default value is "Select All"
                            multi=True,
                            style={
                                'width': '100%',
                                'color': 'black',
                                'backgroundColor': 'white',
                            }
                        )
                    ]),
                    width=6,
                    style={'padding': '0 10px'}
                ),
                
                dbc.Col(
                    html.Div([
                        html.H6('Gender', style={'margin-bottom': '10px'}),  # Header for the Gender dropdown
                        dcc.Dropdown(
                            id='gender-dropdown',
                            options=gender_options,
                            value='all',  # Default value is "All"
                            style={
                                'width': '100%',
                                'color': 'black',
                                'backgroundColor': 'white',
                            }
                        )
                    ]),
                    width=3,
                    style={'padding': '0 5px'}
                ),
                
                dbc.Col(
                    html.Div([
                        html.H6('Sort By', style={'margin-bottom': '10px'}),  # Header for the Sort dropdown
                        dcc.Dropdown(
                            id='sort-dropdown',
                            options=[
                                {'label': 'None', 'value': 'none'},
                                {'label': 'Ascending', 'value': 'asc'},
                                {'label': 'Descending', 'value': 'desc'}
                            ],
                            value='none',
                            style={
                                'width': '100%',
                                'color': 'black',
                                'backgroundColor': 'white',
                            }
                        )
                    ]),
                    width=3,
                    style={'padding': '0 10px'}
                ),
            ],
            align='center',
            style={'margin': '0'}
        )
    ]
)

# Define the output section with cards and charts
output = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Total Students", className="card-title"),
                                    html.P(id='total-students-value', className="card-text", style={'fontSize': '24px'})
                                ]
                            ),
                            style={"margin-bottom": "10px"}  # Spacing between cards
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Male Students", className="card-title"),
                                    html.P(id='male-students-value', className="card-text", style={'fontSize': '24px'})
                                ]
                            ),
                            style={"margin-bottom": "10px"}
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Female Students", className="card-title"),
                                    html.P(id='female-students-value', className="card-text", style={'fontSize': '24px'})
                                ]
                            )
                        ),
                    ],
                    style={"display": "flex", "flexDirection": "column", "gap": "10px"}  # Arrange cards vertically
                ),
                width=4,  # Width of the first column
                style={'padding': '0 20px'}  # Add padding to prevent content from being too close to the edges
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='graduates-bar-chart'
                    )
                ]),
                width=8,  # Width of the second column
                style={'padding': '0 20px'}  # Add padding to prevent content from being too close to the edges
            )
        ],
        style={'padding': '20px 0'}  # Add padding to the row
    )
])

# Define the additional output section with more charts and a data table
additional_output = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='gender-pie-chart'
                    )
                ]),
                width=4,  # Width of the first column
                style={'padding': '0 20px'}  # Add padding to prevent content from being too close to the edges
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='province-line-chart'
                    )
                ]),
                width=4,  # Width of the second column
                style={'padding': '0 20px'}  # Add padding to prevent content from being too close to the edges
            ),
            dbc.Col(
                html.Div([
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{'name': col, 'id': col} for col in df.columns],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left'},
                        page_size=10
                    )
                ]),
                width=4,  # Width of the third column
                style={'padding': '0 20px'}  # Add padding to prevent content from being too close to the edges
            )
        ],
        style={'padding': '20px 0', 'color':'black'}  # Add padding to the row
    )
])

# Define the app layout to include the navbar, header, filters, and output sections
app.layout = html.Div(children=[
    navbar,
    header,
    filter,
    output,
    additional_output  # Add the new output section to the layout
])

# Callback to update the visualizations based on filter and sort inputs
@callback(
    [Output('graduates-bar-chart', 'figure'),
     Output('total-students-value', 'children'),
     Output('male-students-value', 'children'),
     Output('female-students-value', 'children'),
     Output('gender-pie-chart', 'figure'),
     Output('province-line-chart', 'figure'),
     Output('data-table', 'data')],
    [Input('province-dropdown', 'value'),
     Input('gender-dropdown', 'value'),
     Input('sort-dropdown', 'value')]
)
def update_visualizations(selected_provinces, selected_gender, sort_order):
    # Handle "Select All" option for provinces
    if 'all' in selected_provinces:
        selected_provinces = df['schools_province'].unique().tolist()
    
    # Filter data based on selected provinces
    filtered_df = df[df['schools_province'].isin(selected_provinces)]
    
    # Handle "All" option for gender
    if selected_gender == 'all':
        # Compute total counts for both genders
        filtered_df['total'] = filtered_df[['totalmale', 'totalfemale']].sum(axis=1)
        total_students = filtered_df['total'].sum()
        male_students = filtered_df['totalmale'].sum()
        female_students = filtered_df['totalfemale'].sum()
        y_values = 'total'
    else:
        total_students = filtered_df[selected_gender].sum()
        male_students = filtered_df['totalmale'].sum()
        female_students = filtered_df['totalfemale'].sum()
        y_values = selected_gender

    # Apply sorting if needed
    if sort_order == 'none':
        sorted_df = filtered_df
    elif sort_order == 'desc':
        sorted_df = filtered_df.sort_values(by=y_values, ascending=False)
    else:  # sort_order == 'asc'
        sorted_df = filtered_df.sort_values(by=y_values, ascending=True)

    # Create Bar Chart
    bar_fig = px.bar(sorted_df, x='schools_province', y=['totalmale', 'totalfemale'] if selected_gender == 'all' else y_values,
                     title='Number of Graduates by Province and Gender in 2566',
                     labels={'schools_province': 'Province', 'value': 'Number of Students', 'variable': 'Gender'},
                     barmode='group')

    # Create Pie Chart
    gender_counts = filtered_df[['totalmale', 'totalfemale']].sum()
    pie_fig = px.pie(names=['Male', 'Female'], values=gender_counts,
                     title='Gender Distribution of Graduates in 2566')

    # Create Line Chart
    line_fig = px.line(filtered_df, x='schools_province', y=['totalmale', 'totalfemale'],
                       title='Trend of Graduates by Province in 2566',
                       labels={'schools_province': 'Province', 'value': 'Number of Students', 'variable': 'Gender'})

    # Create Data Table
    table_data = filtered_df.to_dict('records')

    return bar_fig, total_students, male_students, female_students, pie_fig, line_fig, table_data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
