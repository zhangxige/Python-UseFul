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


def Customizing_your_plot():
    from bokeh.plotting import figure, show

    # prepare some data
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    y0 = [i**2 for i in x]
    y1 = [10**i for i in x]
    y2 = [10**(i**2) for i in x]

    # create a new plot with a logarithmic axis type
    p = figure(
        title="Logarithmic axis example",
        sizing_mode="stretch_width",
        height=720,
        max_width=1280,
        y_axis_type="log",
        y_range=[0.001, 10 ** 11],
        x_axis_label="sections",
        y_axis_label="particles",
        background_fill_color="#fafafa"
    )
    p.grid.grid_line_color = None

    # add some renderers
    p.line(x, x, legend_label="y=x")
    p.circle(x, x, legend_label="y=x", fill_color="white", size=8)
    p.line(x, y0, legend_label="y=x^2", line_width=3)
    p.line(x, y1, legend_label="y=10^x", line_color="red")
    p.circle(x, y1, legend_label="y=10^x", fill_color="red", line_color="red", size=6)
    p.line(x, y2, legend_label="y=10^x^2", line_color="orange", line_dash="4 4")

    # show the results
    show(p)


def Circle_Map_plot():
    # importing the modules
    from bokeh.plotting import figure, output_file, show
    import math

    # file to save the model 
    output_file("gfg.html") 

    # instantiating the figure object 
    graph = figure(title = "Bokeh Pie Chart") 

    # name of the sectors
    sectors = ["Agriculture", "Industry", "Services"]

    # % tage weightage of the sectors
    percentages = [17.1, 29.1, 53.8]

    # converting into radians
    radians = [math.radians((percent / 100) * 360) for percent in percentages]

    # starting angle values
    start_angle = [math.radians(0)]
    prev = start_angle[0]
    for i in radians[:-1]:
        start_angle.append(i + prev)
        prev = i + prev

    # ending angle values
    end_angle = start_angle[1:] + [math.radians(0)]

    # center of the pie chart
    x = 0
    y = 0

    # radius of the glyphs
    radius = 1

    # color of the wedges
    color = ["yellow", "red", "lightblue"]

    # plotting the graph
    for i in range(len(sectors)):
        graph.wedge(x, y, radius,
                    start_angle = start_angle[i],
                    end_angle = end_angle[i],
                    color = color[i],
                    legend_label = sectors[i])

    # displaying the graph
    show(graph)


if __name__ == '__main__':
    '''
    1、建立画布（生成不同风格）
    2、生成各种类型图标（折线、散点、柱状、饼图）
    3、更改标签
    4、保存图像l
    '''
    Circle_Map_plot()
    pass
