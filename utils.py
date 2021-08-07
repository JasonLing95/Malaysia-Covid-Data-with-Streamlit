import plotly.express as px
import plotly.graph_objects as go

def generate_line_chart(data, y_axis, y_label):
    fig = px.line(data, x='Date', y=y_axis,
              hover_data={"Date": "|%B %d, %Y"})
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=y_label,
        legend_title='State',
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="RebeccaPurple"
        ),
        width=900, 
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

def generate_vaccination_chart(malaysia_reg, malaysia_vaccine):

    df_merge = malaysia_reg.merge(malaysia_vaccine, on='date', how='left').fillna(0)

    # https://github.com/CITF-Malaysia/citf-public/blob/main/static/population.csv
    df_merge['total_population'] = 32657400

    random_x = df_merge['date']
    random_y0 = df_merge['total']
    random_y1 = df_merge['dose1_cumul']
    random_y2 = df_merge['dose2_cumul']
    random_y3 = df_merge['total_population']

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                        mode='lines',
                        name='Total Registered'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                        mode='lines+markers',
                        name='Dose 1 Cumulative'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                        mode='lines+markers', name='Dose 2 Cumulative'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y3,
                        mode='markers', name='Total Population'))

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Cases',
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="RebeccaPurple"
        ),
        width=900, 
        height=500)
    
    return fig