import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Figure:
    """
    Higher level wrapper for plotly, especially focused on time series plots.

    1. Lower level functions
    - Given a series, create the trace
    - e.g. add_line, add_bar, add_scatter
    - Contain all the logic for creating the trace
    - Don't carry **kwargs, keep simple parameters for simplicity

    2. Higher level functions
    - Group lower level functions into a single function
    """

    def __init__(self):
        self.fig = go.Figure()
        self.cmap = px.colors.qualitative.Plotly

    def __call__(self):
        return self.fig

    # Plot settings
    # def set_title_and_axes_labels(self, title, xtitle, ytitle, **kwargs):
    #     self.fig.update_layout(
    #         title={"text": title, "x": 0.5, "y": 0.95},
    #         font=dict(
    #             size=12,
    #         ),
    #         xaxis=dict(
    #             title=xtitle,
    #         ),
    #         yaxis=dict(
    #             title=ytitle,
    #         ),
    #         # legend={"font_size": 10, "orientation": "v", "x": 0.3, "y": 1.11},
    #         uniformtext=dict(mode="hide", minsize=12),
    #         **kwargs,
    #     )

    def xaxes_setting(self, **kwargs):
        self.fig.update_xaxes(**kwargs)

    def set_plot_size(self, width=1350, height=650, **kwargs):
        # ? Add this to init?
        self.fig.update_layout(
            width=width,
            height=height,
            **kwargs,
        )

    def layout(self, **kwargs):
        self.fig.update_layout(
            **kwargs,
        )

    def set_labels_size(self, titlefont_size=20, tickfont_size=17, **kwargs):
        self.fig.update_layout(
            xaxis=dict(
                titlefont_size=titlefont_size,
                tickfont_size=tickfont_size,
            ),
            yaxis=dict(
                titlefont_size=titlefont_size,
                tickfont_size=tickfont_size,
            ),
            **kwargs,
        )

    def annotation(self, x_value, y_value, text, **kwargs):
        self.fig.add_annotation(
            x=x_value,
            y=y_value,
            xref="x",
            yref="y",
            text=text,
            showarrow=True,
            font=dict(size=14, color="#ffffff"),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            ax=5,
            ay=-50,
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#3C4470",
            opacity=0.8,
            **kwargs,
        )

    # Add charts
    # def add_y2(self, title, **kwargs):
    #     self.fig.update_layout(
    #         yaxis2=dict(
    #             title=title,
    #             # titlefont=dict(color="#d62728"),
    #             # tickfont=dict(color="#d62728"),
    #             anchor="x",
    #             overlaying="y",
    #             side="right",
    #             **kwargs,
    #         ),
    #         legend=dict(
    #             x=1.07,
    #             y=1,
    #         ),
    #         **kwargs,
    #     )

    def hbar(self, series, **kwargs):
        self.fig.add_trace(
            go.Bar(
                x=series,
                y=series.index,
                orientation="h",
                name=series.name,
                **kwargs,
            )
        )

    def line(self, series, dash=None, **kwargs):
        self.fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series,
                mode="lines",
                line=dict(width=1.5, dash=dash, **kwargs),
                name=series.name,
            )
        )

    def bar_dataframe(self, x, y, **kwargs):
        # TODO: Document
        self.fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                **kwargs,
            )
        )

    # def line_y2(self, series, yaxis="y2", mode="lines+markers", **kwargs):
    #     self.fig.add_trace(
    #         go.Scatter(
    #             x=series.index,
    #             y=series,
    #             mode=mode,
    #             yaxis=yaxis,
    #             **kwargs,
    #         )
    #     )

    def area(self, series, **kwargs):
        self.fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series,
                mode="lines",
                line=dict(width=1.5),
                fill="tozeroy",
                name=series.name,
                **kwargs,
            )
        )

    def bar(self, series, **kwargs):
        self.fig.add_trace(
            go.Bar(
                x=series.index,
                y=series,
                name=series.name,
                **kwargs,
            )
        )

    def linebar(self, series, color="gray", opacity=0.5, **kwargs):
        # TODO: Fix width (might need to be relative)
        self.fig.add_trace(
            go.Bar(
                x=series.index,
                y=series,
                width=1,
                name=series.name,
                marker=dict(
                    line=dict(width=0.6, color=color),
                    opacity=opacity,
                    color=color,

                    **kwargs,
                ),
            )
        )

    def scatter(self, series, mode="markers", **kwargs):
        self.fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series,
                mode=mode,
                name=series.name,
                **kwargs,
            )
        )

    def dotline(self, series, color="gray", opacity=0.5):
        self.linebar(series, color=color, opacity=opacity)
        self.scatter(series)

    def waterfall(self, df, measure, x_values, text, y_values, orientation="v"):
        #TODO: Document
        """
        DATAFRAME REQUIRES PRE-PROCESSING FOR PLOT
            df: dataframe
            measure(str): realitve or total
            x_values: values in x axis
            y_values(int or float): values in y axis
            text(str): text in the bar
        """
        self.fig.add_trace(
            go.Waterfall(
                name="20",
                orientation=orientation,
                measure=[row for row in df[measure]],
                x=[row for row in df[x_values]],
                textposition="outside",
                text=[row for row in df[text]],
                y=[row for row in df[y_values]],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            )
        )

    def background(self, series, text, color, opacity):
        # TODO: Document
        self.fig.add_vrect(
            x0=series.index.min(),
            x1=series.index.max(),
            annotation_text=text,
            annotation_position="top left",
            fillcolor=color,
            opacity=opacity,
            line_width=0,
            layer="below",
        )

    def time_buttons(self, buttons_dict):
        # TODO: Document
        self.fig.update_xaxes(rangeselector={"buttons": buttons_dict})

    def hline(self, y_value, **kwargs):
        # TODO: Allow list as input or other types
        # TODO: Add vline
        self.fig.add_hline(y=y_value, **kwargs)

    def vline(self, x_value, **kwargs):
        self.fig.add_vline(x=x_value, **kwargs)

    def threshline(self, series, up_thresh, down_thresh, up_color='green', down_color='red'):
        # TODO: Improve colors
        # TODO: Use vline instead

        up_df = series[series > up_thresh].index
        down_df = series[series < down_thresh].index

        for i in up_df:
            self.fig.add_vline(
                x=i,
                line_dash="dot",
                line_color=up_color,
            )

        for i in down_df:
            self.fig.add_vline(
                x=i,
                line_dash="dot",
                line_color=down_color,
            )

    def clear(self):
        self.fig = go.Figure()

    def show(self):
        return self()


class Subplot(Figure):
    # TODO: Document

    """
    Child class of Figure.
    """

    def __init__(self, row, col, **kwargs):
        self.row = row
        self.col = col
        self.fig = make_subplots(rows=self.row, cols=self.col, **kwargs)

    def scatter_subplot(self, series, row, col, mode="markers", **kwargs):
        self.fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series,
                mode=mode,
                **kwargs,
            ),
            row=row,
            col=col,
        )

    def bar_subplot(self, series, row, col, **kwargs):
        self.fig.add_trace(
            go.Bar(
                x=series.index,
                y=series,
                **kwargs,
            ),
            row=row,
            col=col,
        )
