import plotly.express as px

def generate_line_chart(data, y_axis):
    fig = px.line(data, x='Date', y=y_axis,
              hover_data={"Date": "|%B %d, %Y"})
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Cases',
        legend_title='State',
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="RebeccaPurple"
        ),
        width=800, 
        height=500)
    
    return fig

def generate_medical_chart(data, y_axis):
    fig = px.line(data, x="date", y=y_axis,
              hover_data={"date": "|%B %d, %Y"})

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Cases',
        legend_title='Admissions',
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="RebeccaPurple"
        ),
        width=800, 
        height=500)

    return fig