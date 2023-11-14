from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from django.utils import timezone
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas




def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction:transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form})

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'transaction_list.html', {'transactions': transactions})

def generate_pdf_report(transaction):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Transaction_{transaction.id}_report.pdf"'

    # Create the PDF document using ReportLab
    c = canvas.Canvas(response, pagesize=letter)

    # Add the transaction details to the PDF
    c.drawString(50, 750, f'Patient: {transaction.patient.first_name} {transaction.patient.last_name}')
    c.drawString(50, 730, f'Physician: {transaction.physician.first_name} {transaction.physician.last_name}')
    c.drawString(50, 710, f'Reason for Consultation: {transaction.reason_for_consultation}')
    c.drawString(50, 690, f'DOB: {transaction.patient.birthdate}')
    c.drawString(50, 670, f'Age: {transaction.patient.age}')
    c.drawString(50, 650, f'Sex: {transaction.patient.sex}')
    c.drawString(50, 630, f'Room No: {transaction.physician.room_number}')

    # Fetch the VitalSigns related to the Transaction
    vital_signs = transaction.vitalsigns_set.all()

    # Add the VitalSigns details to the PDF
    for i, vital_sign in enumerate(vital_signs):
        c.drawString(50, 610 - (i * 90), f'Temperature: {vital_sign.temperature}')
        c.drawString(50, 590 - (i * 90), f'Respiratory Rate: {vital_sign.respiratory_rate}')
        c.drawString(50, 570 - (i * 90), f'Heart Rate: {vital_sign.heart_rate}')
        c.drawString(50, 550 - (i * 90), f'Blood Pressure: {vital_sign.blood_pressure}')
        c.drawString(50, 530 - (i * 90), f'Oxygen Saturation: {vital_sign.oxygen_saturation}')
        c.drawString(50, 510 - (i * 90), f'Pain Scale: {vital_sign.pain_scale}')
        c.drawString(50, 490 - (i * 90), f'Random Blood Sugar: {vital_sign.random_blood_sugar}')
        c.drawString(50, 470 - (i * 90), f'Remarks: {vital_sign.remarks}')

    c.showPage()
    c.save()

    return response

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import Flowable

class PositionedImage(Flowable):
    def __init__(self, img, x=0, y=0, width=50, height=50):
        Flowable.__init__(self)
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        img = Image(self.img, self.width, self.height)
        img.drawOn(self.canv, self.x, self.y)

class PositionedString(Flowable):
    def __init__(self, text, x=0, y=0, fontName="Helvetica-Bold", fontSize=12):
        Flowable.__init__(self)
        self.text = text
        self.x = x
        self.y = y
        self.fontName = fontName
        self.fontSize = fontSize

    def draw(self):
        self.canv.setFont(self.fontName, self.fontSize)
        self.canv.drawString(self.x, self.y, self.text)

class PositionedTable(Flowable):
    def __init__(self, data, x=0, y=0, colWidths=None, rowHeights=None, style=None):
        Flowable.__init__(self)
        self.data = data
        self.x = x
        self.y = y
        self.colWidths = colWidths
        self.rowHeights = rowHeights
        self.style = style

    def draw(self):
        table = Table(self.data, colWidths=self.colWidths, rowHeights=self.rowHeights)
        if self.style:
            table.setStyle(self.style)
        table.wrapOn(self.canv, self.width, self.height)
        table.drawOn(self.canv, self.x, self.y)



def export_pdf(request, transaction_id):
    # Get the Transaction instance
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # Get the related VitalSigns instances
    vital_signs_list = transaction.vitalsigns_set.all()

    # Prepare data for the table
    styles = getSampleStyleSheet()
    header_style = styles['BodyText']
    header_style.fontSize = 10
    header_style.alignment = 1  # Center alignment

    data = [[Paragraph(column, header_style) for column in ["DATE AND TIME", "TEMP", "RR", "HR", "BP", "O2 SAT", "PAIN", "RBS", "Remarks"]]]

    for vital_signs in vital_signs_list:
        formatted_date_time = vital_signs.date_time.strftime("%m/%d/%Y %I:%M %p")
        remarks = Paragraph(vital_signs.remarks, styles['BodyText'])
        data.append([formatted_date_time, vital_signs.temperature, vital_signs.respiratory_rate, vital_signs.heart_rate, vital_signs.blood_pressure, vital_signs.oxygen_saturation, vital_signs.pain_scale, vital_signs.random_blood_sugar, remarks])

    # Create a table with the data
    table = Table(data)

    # Create a TableStyle and add it to the table
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7),

        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    table = PositionedTable(data, x=25, y=-195, colWidths=[100, 40, 30, 30, 30, 40, 40, 40, 200], rowHeights=None, style=style)

    

    header_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ])
    header = PositionedTable([['PATIENT INFORMATION']], x=25, y=15, colWidths=[550], rowHeights=[15], style=header_style)

    patient_name_paragraph = Paragraph(f'{transaction.patient.last_name.upper()} {transaction.patient.first_name.upper()} {transaction.patient.middle_name.upper()}', styles['BodyText'])
    patient_date_of_birth_paragraph = Paragraph(f'{transaction.patient.birthdate}', styles['BodyText'])
    patient_age_paragraph = Paragraph(f'{transaction.patient.age}', styles['BodyText'])
    header_data = [[patient_name_paragraph, patient_date_of_birth_paragraph, patient_age_paragraph]]
    patient_sex_paragraph = Paragraph(f'{transaction.patient.sex}', styles['BodyText'])
    patient_consul_reason = Paragraph(f'{transaction.reason_for_consultation}', styles['BodyText'])
    header_data_2 = [[patient_sex_paragraph, patient_consul_reason]]
    patient_physician = Paragraph(f'{transaction.physician.first_name} {transaction.physician.last_name}', styles['BodyText'])
    patient_room_number = Paragraph(f'{transaction.physician.room_number}', styles['BodyText'])
    header_data_3 = [[patient_physician, patient_room_number]]
    

    patient_info_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ])
    patient_info = PositionedTable(header_data, x=25, y=-25, colWidths=[300, 150, 100], rowHeights=[40], style=patient_info_style)
    patient_info_2 = PositionedTable(header_data_2, x=25, y=-75, colWidths=[100, 450], rowHeights=[50], style=patient_info_style)
    patient_info_3 = PositionedTable(header_data_3, x=25, y=-115, colWidths=[275, 275], rowHeights=[40], style=patient_info_style)


    # Create the PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0)
    elements = []

    img = PositionedImage('media/OPD Logo.jpg', x=-20, y=70, width=250, height=50)
    out_patient_dept = PositionedString('OUT-PATIENT DEPARTMENT', x=200, y=50)
    vs_sheet = PositionedString('VITAL SIGNS SHEET', x=220, y=35)
    
 
    elements.append(img)
    elements.append(out_patient_dept)
    elements.append(vs_sheet)
    elements.append(header)
    elements.append(patient_info)
    elements.append(patient_info_2)
    elements.append(patient_info_3)

    patient_name = PositionedString('PATIENT NAME', x=27, y=4)
    elements.append(patient_name)

    date_of_birth = PositionedString('DATE OF BIRTH', x=327, y=4)
    elements.append(date_of_birth)

    patient_age = PositionedString('AGE', x=477, y=4)
    elements.append(patient_age)

    patient_sex = PositionedString('SEX', x=27, y=-36)
    elements.append(patient_sex)

    reason_for_consul = PositionedString('REASON FOR CONSULTATION', x=127, y=-36)
    elements.append(reason_for_consul)

    physician = PositionedString('PHYSICIAN', x=27, y=-86)
    elements.append(physician)

    room_number = PositionedString('ROOM NO.', x=302, y=-86)
    elements.append(room_number)

    # Add the table
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    patient_full_name = f"{transaction.patient.first_name.upper()} {transaction.patient.last_name.upper()}"
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={patient_full_name} vital signs.pdf'


    return response

