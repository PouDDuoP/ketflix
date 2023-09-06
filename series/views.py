from datetime import datetime
from io import BytesIO
import os
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4

from series.models import Serie, Episode
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch

from reportlab.graphics.shapes import Drawing, Rect, String, Group, Line
from reportlab.graphics.widgets.markers import makeMarker

# Create your views here.
class SerieView(View):

    def get(self, request): 
        if request.user.is_authenticated:
            context = {
                'series' : list(Serie.objects.all())
            }
        
            return render(request, 'series.html', context=context)
        return redirect('login')
        
class EpisodeView(LoginRequiredMixin, View):

    def get(self, request, serie_id: int): 
        context = {
            'episodes' : list(Episode.objects.filter(serie_id=serie_id))
        }
        
        return render(request, 'episodes.html', context=context)
    
class ReportView(View):

    # def get(self, request): 
    #     context = {
    #         'series' : list(Serie.objects.all())
    #     }
    
    #     return render(request, 'series.html', context=context)
    
    # def get(self, request):         
    #     response = HttpResponse(content_type='application/pdf')
    #     d = datetime.today().strftime('%Y-%m-%d') 
    #     response['Content-Disposition'] = f'inline; filename="{d}.pdf'
        
    #     buffer = BytesIO()
    #     p = canvas.Canvas(buffer, pagesize=A4)
        
    #     #Data to print
    #     data = {
    #         "Posts":[{"title":"Python","views":500},{"title":"JavaScript","views":500}],
    #         "Videos":[{"title":"Python Programming", "likes":500}], "Blogs":[{"name":"Report Lab", "likes": 500, "claps":500}],
    #         }
        
    #     # Start writing the PDF here
    #     p.setFont("Helvetica", 15, leading=None) 
    #     p.setFillColorRGB(0.29296875, 0.453125,0.609375)
    #     p.drawString(260,800,"My Website") 
    #     p.line(0,780, 1000, 780)
    #     p.line(0,778,1000,778)
    #     x1 = 20
    #     y1 = 750
        
    #     #Render data
    #     for k,v in data.items():
    #         p.setFont("Helvetica", 15, leading=None)
    #         p.drawString(x1,y1-12,f"{k}")
    #         for value in v:
    #             for key, val in value.items():
    #                 p.setFont("Helvetica", 10, leading=None)
    #                 p.drawString(x1,y1-20, f" {key} - {val}")
    #                 y1 = y1-60
        
    #     p.setTitle(f'Report on {d}')
    #     p.showPage()
    #     p.save()
        
    #     pdf = buffer.getvalue()
    #     buffer.close()
    #     response.write(pdf)
        
    #     return response
    
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        d = datetime.today().strftime('%Y-%m-%d') 
        response['Content-Disposition'] = f'inline; filename="{d}.pdf'
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        doc = SimpleDocTemplate('test.pdf', pagesize=A4)
        
        story = []
        estilo = getSampleStyleSheet()

        #EJEMPLO 01: Dibujando alguna forma y texto
        #==========
        # d = Drawing(400, 200)

        # r =(Rect(50, 50, 300, 100, fillColor=colors.yellow))
        # r.strokeColor = colors.red  # otra forma de agregar propiedades
        # r.strokeWidth = 3
        # d.add(r)

        # d.add(String(150,100, 'Hola mundo', fontSize=18, fillColor=colors.red))
        # d.add(String(180,86, 'Caracteres especiales: \
        #             \xc2\xa2\xc2\xa9\xc2\xae\xc2\xa3\xce\xb1\xce\xb2',
        #             fillColor=colors.red))
        # story.append(d)
        # #Entre las distintas formas tenemos: Rect, Circle, Ellipse, Wedge, Polygon,
        # #Line, PolyLine, String, Group, 


        # #EJEMPLO 02: Obteniendo propiedades
        # #==========
        # #Esto es un buena forma de saber las propiedades de los elementos que usemos,
        # #usaremos pprint que nos lo mostrará en el shell
        # import pprint
        # r = Rect(0, 0, 200, 100)
        # pprint.pprint(r.getProperties())

        # #EJEMPLO 03: Label
        # #==========
        # from reportlab.graphics.charts.textlabels import Label

        # d = Drawing(200, 100)
        # lab = Label()
        # lab.setOrigin(100,90)
        # lab.angle = 45
        # lab.dx = 0  # desplazamiento en x
        # lab.dy = -20  # desplazamiento en y
        # lab.boxStrokeColor = colors.green
        # lab.setText('Un \nLabel \nMulti-Linea')
        # d.add(lab)
        # pprint.pprint(lab.getProperties())  # tiene muchas más propiedades
        # story.append(d)

        # #EJEMPLO 04: Ejes
        # #===========
        # #Nota: Aquí los datos aún no se muestran
        # from reportlab.graphics.charts.axes import XCategoryAxis,YValueAxis
        # d = Drawing(400, 200)
        # data = [(10, 20, 30, 40), (15, 22, 37, 42)]

        # xAxis = XCategoryAxis()
        # xAxis.setPosition(75, 75, 300)  # x, y, ancho
        # xAxis.configure(data)
        # xAxis.categoryNames = ['Oso', 'Tigre', 'León', 'Camaleón']
        # xAxis.labels[2].dy = -15
        # xAxis.labels[2].angle = 30
        # xAxis.labels[2].fontName = 'Times-Bold'

        # yAxis = YValueAxis()
        # yAxis.setPosition(50, 80, 125)
        # yAxis.configure(data)
        # d.add(xAxis)
        # d.add(yAxis)

        # story.append(d)
        # story.append(PageBreak())

        # #EJEMPLO 05: Gráfico de Barras
        # #===========
        # from reportlab.graphics.charts.barcharts import VerticalBarChart

        # d = Drawing(400, 200)
        # data = [
        #         (13, 5, 20, 22, 37, 45, 19, 4),
        #         (14, 6, 21, 23, 38, 46, 20, 5)
        #         ]
        # bc = VerticalBarChart()
        # bc.x = 50
        # bc.y = 50
        # bc.height = 125
        # bc.width = 300
        # bc.data = data
        # bc.strokeColor = colors.black
        # bc.valueAxis.valueMin = 0
        # bc.valueAxis.valueMax = 50
        # bc.valueAxis.valueStep = 10  #paso de distancia entre punto y punto
        # bc.categoryAxis.labels.boxAnchor = 'ne'
        # bc.categoryAxis.labels.dx = 8
        # bc.categoryAxis.labels.dy = -2
        # bc.categoryAxis.labels.angle = 30
        # bc.categoryAxis.categoryNames = ['Ene-14','Feb-14','Mar-14',
        #     'Abr-14','May-14','Jun-14','Jul-14','Ago-14']
        # bc.groupSpacing = 10
        # bc.barSpacing = 2
        # #bc.categoryAxis.style = 'stacked'  # Una variación del gráfico
        # d.add(bc)
        # pprint.pprint(bc.getProperties())
        # story.append(d)

        # #EJEMPLO 06: Gráfico linear
        # #==========
        # from reportlab.graphics.charts.linecharts import HorizontalLineChart

        # titulo = Paragraph("Calificaciones Informática", estilo['title'])
        # story.append(titulo)
        # story.append(Spacer(0, inch*.1))

        # d = Drawing(400, 200)
        # lc = HorizontalLineChart()
        # lc.x = 30
        # lc.y = 50
        # lc.height = 125
        # lc.width = 350
        # lc.data = [[8,10,5,2]]
        # lc.categoryAxis.categoryNames = ['Suspenso', 'Aprobado', 'Notable', 
        #                                 'Sobresaliente']
        # lc.categoryAxis.labels.boxAnchor = 'n'
        # lc.valueAxis.valueMin = 0
        # lc.valueAxis.valueMax = 12
        # lc.valueAxis.valueStep = 2  # Los pasos pueden ser tambien [10, 15, 30, 35, 40]
        # lc.lines[0].strokeWidth = 2
        # lc.lines[0].symbol = makeMarker('FilledCircle') # círculos rellenos
        # lc.lines[1].strokeWidth = 1.5
        # d.add(lc)
        # story.append(d)

        # #EJEMPLO 07: Trazos lineales
        # #==========
        from reportlab.graphics.charts.lineplots import LinePlot

        d = Drawing(400, 50)
        data = [
            ((1,1), (2,2), (2.5,1), (3,3), (10,6)),
            ((1,2), (2,3), (2.5,2), (3.5,5), (10,3))
        ]
        lp = LinePlot()
        lp.x = 0
        lp.y = 0
        lp.height = 125
        lp.width = 400
        lp.data = data
        lp.joinedLines = 1
        lp.fillColor = colors.white
        lp.lines[0].symbol = makeMarker('FilledCircle')
        lp.lines[1].symbol = makeMarker('Circle')
        lp.lineLabelFormat = '%2.0f'
        lp.strokeColor = colors.black
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = 15
        lp.xValueAxis.valueSteps = [1, 2, 2.5, 3, 4, 5, 10]
        lp.xValueAxis.labelTextFormat = '%2.1f'
        lp.yValueAxis.valueMin = 0
        lp.yValueAxis.valueMax = 10
        lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6, 8]


        #Veamos como se inserta las leyendas. En este caso usaremos el LineLegend,
        #que son leyendas en linea.
        from reportlab.graphics.charts.legends import LineLegend

        legend = LineLegend()
        legend.fontSize = 8
        legend.alignment = 'right'
        legend.x = 0
        legend.y = -50
        legend.columnMaximum = 2
        legend.fontName  = 'Helvetica'

        #Definimos nuestras etiquetas  y usamos los colores del propio gráfico.
        etiquetas  = ['Opcion 01', 'Opcion 02']
        legend.colorNamePairs  = [(lp.lines[i].strokeColor, etiquetas[i]) for i in range(len(lp.data))]

        d.add(lp)
        d.add(legend)
        story.append(d)


        #EJEMPLO 08: Gráficos Circulares
        #==========
        # from reportlab.graphics.charts.piecharts import Pie

        # d = Drawing(300, 200)
        # pc = Pie()
        # pc.x = 65
        # pc.y = 15
        # pc.width = 170
        # pc.height = 170
        # pc.data = [10,20,30,40,50]
        # pc.labels = ['IE','Kopete','Chrome','Firefox','Opera']

        # pc.slices.strokeWidth=0.5
        # pc.slices[3].popout = 10
        # pc.slices[3].strokeWidth = 2
        # pc.slices[3].strokeDashArray = [2,2]
        # pc.slices[3].labelRadius = 1.75
        # pc.slices[3].fontColor = colors.red
        # pc.sideLabels = 1  # Con 0 no se muestran líneas hacia las etiquetas
        # #~ pc.slices.labelRadius = 0.65  # Para mostrar el texto dentro de las tajadas

        # #Insertamos la legenda

        # from reportlab.graphics.charts.legends import Legend
        # legend = Legend() 
        # legend.x               = 370 
        # legend.y               = 0 
        # legend.dx              = 8  
        # legend.dy              = 8  
        # legend.fontName        = 'Helvetica'  
        # legend.fontSize        = 7  
        # legend.boxAnchor       = 'n'  
        # legend.columnMaximum   = 10  
        # legend.strokeWidth     = 1  
        # legend.strokeColor     = colors.black  
        # legend.deltax          = 75  
        # legend.deltay          = 10  
        # legend.autoXPadding    = 5  
        # legend.yGap            = 0  
        # legend.dxTextSpace     = 5  
        # legend.alignment       = 'right'  
        # legend.dividerLines    = 1|2|4  
        # legend.dividerOffsY    = 4.5  
        # legend.subCols.rpad    = 30  

        # #Insertemos nuestros propios colores
        # colores  = [colors.blue, colors.red, colors.green, colors.yellow, colors.pink]
        # for i, color in enumerate(colores): 
        #     pc.slices[i].fillColor = color
            
        # legend.colorNamePairs  = [(
        #                             pc.slices[i].fillColor, 
        #                             (pc.labels[i][0:20], '%0.2f' % pc.data[i])
        #                         ) for i in range(len(pc.data))]

        # d.add(pc) 
        # d.add(legend)
        # story.append(d)

        # #EJEMPLO 09: Usando Grupo
        # #==========
        # d = Drawing(400, 200)
        # Ejes = Group(
        #     Line(0,0,100,0),  # eje x
        #     Line(0,0,0,50),   # eje y
        #     Line(0,10,10,10), # Marcas en el eje y
        #     Line(0,20,10,20),
        #     Line(0,30,10,30),
        #     Line(0,40,10,40),
        #     Line(10,0,10,10), # Marcas en el eje x
        #     Line(20,0,20,10),
        #     Line(30,0,30,10),
        #     Line(40,0,40,10),
        #     Line(50,0,50,10),
        #     Line(60,0,60,10),
        #     Line(70,0,70,10),
        #     Line(80,0,80,10),
        #     Line(90,0,90,10),
        #     String(20, 35, 'Ejes', fill=colors.black)
        #     )

        # PrimerGrupoEjes = Group(Ejes)
        # PrimerGrupoEjes.translate(10,10)
        # d.add(PrimerGrupoEjes)

        # SegundoGrupoEjes = Group(Ejes)
        # SegundoGrupoEjes.translate(150,10)
        # SegundoGrupoEjes.rotate(15)
        # d.add(SegundoGrupoEjes)

        # TercerGrupoEjes = Group(Ejes)
        # TercerGrupoEjes.translate(300,10)
        # TercerGrupoEjes.rotate(30)
        # d.add(TercerGrupoEjes)

        # story.append(d)

        doc.build(story)
        os.system('test.pdf')
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response

    
        # return render(request, 'series.html', context=context)
        