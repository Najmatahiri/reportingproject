from reportlab.lib.validators import Auto, colors
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from django.templatetags.static import static
from reportlab.lib.pagesizes import  A4
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.graphics.shapes import Drawing, String
from datetime import datetime
from reportlab.graphics.charts.barcharts import VerticalBarChart

APP_ROOT = "reporting"
width, height = A4


def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = "right"
    legend.x = 50
    legend.y = 150
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


def pie_chart_with_legend(data, title, chart, legend=False):
    labels = ["Patched", "Not Patched"]
    data = data
    drawing = Drawing(width=200, height=150)
    my_title = String(170, 40, title, fontSize=15)
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
    if legend:
        add_legend(drawing, chart, data)
    return drawing


def create_table(data, canv, x, y):
    table = Table(data=data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )
    table.wrap(900, 900)
    table.drawOn(canv, x, y)


def create_header(canv):
    image_path = APP_ROOT + static("images/absLogo1.jpg")
    logo = Image(image_path, width=100, height=100)
    logo.hAlign = "LEFT"
    logo.drawOn(canv, 10, 750)
    date_style = ParagraphStyle(name="default", fontSize=12, leading=24)
    current_date = datetime.today().strftime("%d-%m-%Y")
    date = Paragraph(f"Date : {current_date}", date_style)
    date.wrap(300, 500)
    date.drawOn(canv, 450, 780)
    canv.line(10, 780, 570, 780)


def create_footer(canv, page_number):
    canv.line(10, 100, 570, 100)
    canv.drawString(20, 80, "Société Général African Business Services")
    canv.drawString(
        20,
        65,
        "Boulevard Sidi Mohamed Ben Abdellah, Tour Ivoire 2 - Marina, 20030- Casablanca ",
    )
    canv.drawCentredString(width / 2, 25, f"- Page {page_number} -")


def create_bar_chart(data, category_names, canv, x, y):
    drawing1 = Drawing(400, 200)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 50
    bar.height = 125
    bar.width = 300
    bar.data = data
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = 1000
    bar.valueAxis.valueStep = 100
    bar.categoryAxis.labels.boxAnchor = "ne"
    bar.categoryAxis.labels.dx = 8
    bar.categoryAxis.labels.dy = -2
    bar.categoryAxis.labels.angle = 30
    bar.barSpacing = 2
    bar.bars[0].fillColor = colors.green
    bar.bars[1].fillColor = colors.red
    bar.categoryAxis.categoryNames = category_names
    drawing1.add(bar)
    drawing1.drawOn(canv, x, y)


def create_section_title(title, styles, canv, x, y):
    heading_style = styles["Heading3"]
    titre_section_5 = Paragraph(f"- {title}", heading_style)
    titre_section_5.wrap(900, 200)
    titre_section_5.drawOn(canv, x, y)


def create_table_for_more_info(data, canv, x, y):
    table = Table(data)
    style = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add borders to all cells
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center align all cells
        ]
    )
    table.setStyle(style)
    table.wrap(300, 300)
    table.drawOn(canv, x, y)


def create_header_details_paragraph(title, text, styles, canv, x, y, text_add_x):
    detail_left = Paragraph(f"{title}: ", styles["Heading4"])

    detail_left.wrap(300, 500)
    detail_left.drawOn(canv, x, y)

    detail_right = Paragraph(
        text, ParagraphStyle("detail_title", fontSize=9, leading=24)
    )
    detail_right.wrap(300, 500)
    x_detail = x + text_add_x
    y_detail = y - 12
    detail_right.drawOn(canv, x_detail, y_detail)
