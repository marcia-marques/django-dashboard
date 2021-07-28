from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d, ColumnDataSource, LinearAxis, HoverTool
from bokeh.layouts import column, Spacer, row, grid


def bokeh_raw(df, color='#1f77b4'):

    # source
    source = ColumnDataSource(df)

    myvars = []
    for var in ['CO', 'CO2', 'CH4', 'H2O', 'Press', 'ALARM']:
        myvars += [x for x in df.columns if var in x]
    myvars = list(dict.fromkeys(myvars))

    # hover tool
    hover_tool_p = HoverTool(
        tooltips=[('date', '@DATE_TIME{%m/%d/%Y %H:%M:%S}'),
                  ('value', '$y')],
        formatters={'@DATE_TIME': 'datetime'})

    plots = []
    for myvar in myvars:
        p = figure(plot_height=100,
                   plot_width=900,
                   toolbar_location=None,
                   x_axis_type="datetime",
                   x_axis_location="below")
        p.line(x='DATE_TIME', y=myvar, legend_label=myvar,
               source=source, line_color=color)
        p.add_tools(hover_tool_p)
        p.xaxis.visible = False
        p.legend.background_fill_alpha = 0.75
        p.legend.spacing = 0
        p.legend.padding = 2
        plots.append(p)

    a = column(*plots)
    my_layout = grid([a], ncols=1)
    script, div = components(my_layout)

    return script, div


def bokeh_dashboard(df, var1, var2):

    p1 = time_series(df, var1, var2)
    p2 = scatter_plot(df, var1, var2)
    p3 = box_plot(df, var1)
    p4 = weekday_plot(df, var1)

    a = column(row(p1), Spacer(height=20), row(p2, p3, p4))
    my_layout = grid([a], ncols=1)
    script, div = components(my_layout)

    return script, div


def time_series(df, var1, var2, color1='#1f77b4', color2='#ff7f0e'):

    # source
    source = ColumnDataSource(df)

    # hover tool
    hover_tool_p = HoverTool(
        tooltips=[('date', '@DATE_TIME{%m/%d/%Y %H}'),
                  ('value', '$y')],
        formatters={'@DATE_TIME': 'datetime'})

    # plot
    p = figure(
        plot_height=300,
        plot_width=990,
        tools="pan, ywheel_zoom, box_zoom, reset, save",
        toolbar_location='above',
        x_axis_type="datetime",
        x_axis_location="below")

    # left y axis plot
    if df[var1].count() != 0:
        p.y_range = Range1d(
            start=df[var1].min(), end=df[var1].max())
        p.line(x='DATE_TIME', y=var1, source=source, line_color=color1)

    # right y axis plot
    if df[var2].count() != 0:
        p.extra_y_ranges = {
            "y2": Range1d(start=df[var2].min(), end=df[var2].max())}
        p.add_layout(LinearAxis(y_range_name="y2"), 'right')
        p.line(x='DATE_TIME', y=var2, source=source,
               y_range_name="y2", line_color=color2)
    else:
        p.extra_y_ranges = {"y2": Range1d(start=0, end=0)}
        p.add_layout(LinearAxis(y_range_name="y2"), 'right')

    p.yaxis[0].axis_label = var1
    p.yaxis[0].axis_label_text_color = color1
    p.yaxis[1].axis_label = var2
    p.yaxis[1].axis_label_text_color = color2
    p.xaxis.axis_label = 'Date (Local Time)'
    p.add_tools(hover_tool_p)
    p.toolbar.logo = None

    return p


def scatter_plot(df, var1, var2, color1='#1f77b4', color2='#ff7f0e'):

    # hover tool
    hover_tool_p = HoverTool(
        tooltips=[('value y', '$y'),
                  ('value x', '$x')])

    # plot
    p = figure(plot_height=320,
               plot_width=320,
               tools="pan, ywheel_zoom, box_zoom, reset, save",
               toolbar_location='above')

    if df[var1].count() != 0 and df[var2].count() != 0:
        p.scatter(x=df[var2], y=df[var1],
                  color=color1, size=4, fill_alpha=0.6)

    p.yaxis[0].axis_label = var1
    p.xaxis[0].axis_label = var2
    p.yaxis[0].axis_label_text_color = color1
    p.xaxis[0].axis_label_text_color = color2
    p.add_tools(hover_tool_p)
    p.toolbar.active_inspect = None
    p.toolbar.logo = None

    return p


def box_plot(df, var1, color1='#1f77b4'):

    # dataframe
    df['hour'] = df.DATE_TIME.dt.strftime('%H')
    hours = [str(x).zfill(2) for x in range(0, 24)]

    # find the quartiles and IQR for each category
    groups = df[['hour', var1]].groupby('hour')
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    # find the outliers for each category
    def outliers(group):
        cat = group.name
        return group[(
            group[var1] > upper.loc[cat][var1]) | (
            group[var1] < lower.loc[cat][var1])][var1]
    out = groups.apply(outliers).dropna()

    # prepare outlier data for plotting, we need coordinates
    # for every outlier
    if not out.empty:
        out_x = []
        out_y = []
        for keys in out.index:
            out_x.append(keys[0])
            out_y.append(out.loc[keys[0]].loc[keys[1]])

    # if no outliers, shrink lengths of stems to be no longer
    # than the minimums or maximums
    q_min = groups.quantile(q=0.00)
    q_max = groups.quantile(q=1.00)
    upper[var1] = [min([x, y]) for (x, y) in zip(
        list(q_max.loc[:, var1]), upper[var1])]
    lower[var1] = [max([x, y]) for (x, y) in zip(
        list(q_min.loc[:, var1]), lower[var1])]

    p = figure(plot_height=320,
               plot_width=320,
               x_range=hours,
               tools="pan, ywheel_zoom, box_zoom, reset, save",
               toolbar_location='above')

    if df[var1].count() != 0:

        # stems
        p.segment(hours, upper[var1], hours, q3[var1], line_color="black")
        p.segment(hours, lower[var1], hours, q1[var1], line_color="black")

        # boxes
        p.vbar(hours, 0.7, q2[var1], q3[var1],
               fill_color=color1, line_color="black")
        p.vbar(hours, 0.7, q1[var1], q2[var1],
               fill_color=color1, line_color="black")

        # whiskers (almost-0 height rects simpler than segments)
        p.rect(hours, lower[var1], 0.2, 0.00001, line_color="black")
        p.rect(hours, upper[var1], 0.2, 0.00001, line_color="black")

        # outliers
        if not out.empty:
            p.circle(out_x, out_y, size=4, color=color1, fill_alpha=0.6)

    p.xaxis.major_label_text_font_size = "8px"
    p.yaxis[0].axis_label = var1
    p.yaxis[0].axis_label_text_color = color1
    p.xaxis.axis_label = 'Local Time'
    p.toolbar.logo = None

    return p


def weekday_plot(df, var1, color1='#1f77b4'):

    # dataframe
    df['hour'] = df.DATE_TIME.dt.strftime('%H')
    df['weekday'] = (df.DATE_TIME.dt.weekday < 5).astype(float)
    df['weekday'] = df['weekday'].map({1.0: 'weekday', 0.0: 'weekend'})
    groups_week = df[['hour', 'weekday', var1]].groupby(['hour', 'weekday'])
    hours = [str(x).zfill(2) for x in range(0, 24)]

    # hoover tool
    hover_tool_p = HoverTool(
        tooltips=[('value y', '$y')])

    p = figure(plot_height=320,
               plot_width=320,
               x_range=hours,
               tools="pan, ywheel_zoom, box_zoom, reset, save",
               toolbar_location='above')

    if df[var1].count() != 0:

        if 'weekday' in df.weekday.values:
            p.line(x=hours, y=groups_week[var1].mean().loc[:, 'weekday'],
                   color=color1, legend_label='weekday', line_width=1.5)
        if 'weekend' in df.weekday.values:
            p.line(x=hours, y=groups_week[var1].mean().loc[:, 'weekend'],
                   color=color1, legend_label='weekend', line_width=1.5,
                   alpha=0.5)

    p.xaxis.major_label_text_font_size = "8px"
    p.yaxis[0].axis_label = var1
    p.yaxis[0].axis_label_text_color = '#1f77b4'
    p.xaxis.axis_label = 'Local Time'
    p.add_tools(hover_tool_p)
    p.toolbar.active_inspect = None
    p.toolbar.logo = None
    p.legend.label_text_font_size = "8pt"
    p.legend.click_policy = "hide"
    p.legend.spacing = 0
    p.legend.padding = 2
    p.legend.background_fill_alpha = 0.75

    return p
