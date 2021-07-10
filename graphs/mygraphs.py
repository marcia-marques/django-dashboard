from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d, ColumnDataSource, LinearAxis, HoverTool


def time_series(df):

    # source
    source = ColumnDataSource(df)

    # variables
    var1 = 'CO2_dry_m'
    var2 = 'CH4_dry_m'

    # Hover tools
    hover_tool_p = HoverTool(
        tooltips=[('date', '@DATE_TIME{%Y-%m-%d %H}'),
                  ('value', '$y')],
        formatters={'@DATE_TIME': 'datetime'},
    )

    # plot
    p = figure(
        plot_height=300,
        plot_width=990,
        tools="pan, ywheel_zoom, box_zoom, reset, save",
        toolbar_location='above',
        x_axis_type="datetime",
        x_axis_location="below")

    # Left y axis plot
    if df[var1].count() != 0:
        p.y_range = Range1d(
            start=df[var1].min(), end=df[var1].max())
        p.line(x='DATE_TIME', y=var1, source=source, line_color='#1f77b4')
    p.yaxis[0].axis_label = var1
    p.yaxis[0].axis_label_text_color = '#1f77b4'

    # Right y axis plot
    if df[var2].count() != 0:
        p.extra_y_ranges = {
            "y2": Range1d(start=df[var2].min(), end=df[var2].max())}
        p.add_layout(LinearAxis(y_range_name="y2"), 'right')
        p.line(x='DATE_TIME', y=var2, source=source,
               y_range_name="y2", line_color='#ff7f0e')
    else:
        p.extra_y_ranges = {"y2": Range1d(start=0, end=0)}
        p.add_layout(LinearAxis(y_range_name="y2"), 'right')

    p.yaxis[1].axis_label = var2
    p.yaxis[1].axis_label_text_color = '#ff7f0e'

    p.add_tools(hover_tool_p)
    p.toolbar.logo = None
    p.xaxis.axis_label = 'Date (Local Time)'

    script, div = components(p)

    # return {'script': script, 'div': div}
    return script, div
