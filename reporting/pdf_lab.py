from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.validators import Auto, colors
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.doughnut import Doughnut
from reportlab.graphics.shapes import Drawing, String
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle


def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 100
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


def pie_chart_with_legend(data, title, chart):
    labels = ["Patched", "Not Patched"]
    data = data
    drawing = Drawing(width=200, height=150)
    my_title = String(170, 40, title, fontSize=14)
    chart.sideLabels = True
    chart.x = 150
    chart.y = 65
    chart.data = data
    chart.slices[0].fillColor = colors.green
    chart.slices[1].fillColor = colors.red
    chart.labels = labels
    chart.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(chart)
    add_legend(drawing, chart, data)
    return drawing


def create_table(data):
    # Définition des données pour le tableau

    # Création du tableau
    table = Table(data)

    # Définition du style du tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('SPAN', (0, 0), (-1, 0)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),

    ])
    table.setStyle(style)

    return table


def data_table(pathed, not_pateched, entete):
    total = pathed + not_pateched
    datable = [
        [entete],
        ["PATCHED", pathed],
        ["NOT PATCHED", not_pateched],
        ["", total]

    ]

    return datable
