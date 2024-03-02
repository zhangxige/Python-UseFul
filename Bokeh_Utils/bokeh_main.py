# ref: https://docs.bokeh.org/en/latest/index.html
from bokeh.plotting import figure, show


def Creating_a_simple_line_chart():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y1 = [6, 7, 2, 4, 5]
    y2 = [2, 3, 4, 5, 6]
    y3 = [4, 5, 5, 7, 2]

    # create a new plot with a title and axis labels
    p = figure(title="MultipleLineExample", x_axis_label="x", y_axis_label="y")

    # add multiple renderers
    p.line(x, y1, legend_label="Temp.", color="blue", line_width=2)
    p.line(x, y2, legend_label="Rate", color="red", line_width=2)
    p.line(x, y3, legend_label="Objects", color="green", line_width=2)

    # show the results
    show(p)


def Adding_and_customizing_renderers():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [4, 5, 5, 7, 2]

    # create a new plot with a title and axis labels
    p = figure(
        title="Glyphs properties example",
        x_axis_label="x",
        y_axis_label="y"
        )

    # add circle renderer with additional arguments
    circle = p.circle(
        x,
        y,
        legend_label="Objects",
        fill_color="red",
        fill_alpha=0.5,
        line_color="blue",
        size=80,
    )

    # change color of previously created object's glyph
    glyph = circle.glyph
    glyph.fill_color = "blue"

    # show the results
    show(p)


def Adding_legends_text_and_annotations():
    from bokeh.plotting import figure, show

    # prepare some data
    x = [1, 2, 3, 4, 5]
    y1 = [4, 5, 5, 7, 2]
    y2 = [2, 3, 4, 5, 6]

    # create a new plot
    p = figure(title="Legend example")

    # add circle renderer with legend_label arguments
    line = p.line(x, y1, legend_label="Temp.", line_color="blue", line_width=2)
    circle = p.circle(
        x,
        y2,
        legend_label="Objects",
        fill_color="red",
        fill_alpha=0.5,
        line_color="blue",
        size=80,
    )

    # display legend in top left corner (default is top right corner)
    p.legend.location = "top_left"

    # add a title to your legend
    p.legend.title = "Obervations"

    # change appearance of legend text
    p.legend.label_text_font = "times"
    p.legend.label_text_font_style = "italic"
    p.legend.label_text_color = "navy"

    # change border and background of legend
    p.legend.border_line_width = 3
    p.legend.border_line_color = "navy"
    p.legend.border_line_alpha = 0.8
    p.legend.background_fill_color = "navy"
    p.legend.background_fill_alpha = 0.2

    # show the results
    show(p)


if __name__ == '__main__':
    '''
    1、建立画布（生成不同风格）
    2、生成各种类型图标（折线、散点、柱状、饼图）
    3、更改标签
    4、保存图像l
    '''
    Adding_legends_text_and_annotations()
    pass
