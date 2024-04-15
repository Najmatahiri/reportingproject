from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.validators import Auto,colors
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String
from reportlab.platypus import SimpleDocTemplate, Paragraph


def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 100
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


def pie_chart_with_legend(data, title):
    labels = ["Prod", "Hors Prod"]
    data = data
    drawing = Drawing(width=200, height=150)
    my_title = String(170, 40, title, fontSize=14)
    pie = Pie()
    pie.sideLabels = True
    pie.x = 150
    pie.y = 65
    pie.data = data
    pie.slices[0].fillColor = colors.green
    pie.slices[1].fillColor = colors.red
    pie.labels = labels
    pie.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(pie)
    add_legend(drawing, pie, data)
    return drawing


