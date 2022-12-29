import boto3
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


FONT_XL = 26
FONT_L = 24
FONT_M = 16 
FONT_S = 14
FONT_XS = 12
FONT_XXS = 10

def draw_hr(doc, vertical_offset):
    doc.setStrokeColor('gray')
    doc.setLineWidth(1)
    doc.line(75, vertical_offset, 550, vertical_offset)
    doc.setStrokeColor('black')

def write_invoice_title(doc):
    doc.setFont('Times-Bold', FONT_L)
    doc.drawString(50, 50, 'Invoice')

def write_seller_details(doc, name, line1, city, state, country, postal_code,
                             number, email ):
    doc.setFont('Times-Bold', FONT_M)
    doc.drawString(75, 130, name)
    doc.setFont('Times-Roman', FONT_XS)
    doc.drawString(75, 145, line1)
    doc.drawString(75, 160, f'{city} {state}, {postal_code}')
    doc.drawString(75, 175, country)
    doc.drawString(75, 190, number)
    doc.drawString(75, 205, email)

def write_customer_details(doc, name, line1, city, state, country, postal_code, email ):
    doc.setFont('Times-Bold', FONT_M)
    doc.drawString(225, 130, 'Billed To')
    doc.setFont('Times-Roman', FONT_XS)
    doc.drawString(225, 145, name)
    doc.drawString(225, 160, line1)
    doc.drawString(225, 175, f'{city} {state}, {postal_code}')
    doc.drawString(225, 190, country)
    doc.drawString(225, 205, email)

def write_invoice_details(doc, invoice_number, issue_date, due_date):
    doc.setFont('Times-Bold', FONT_M)
    doc.drawString(375, 130, 'Invoice Details')
    doc.setFont('Times-Roman', FONT_XS)
    doc.drawString(375, 145, f'Invoice No. {invoice_number}')
    doc.drawString(375, 160, f'Date Issued {issue_date.replace("-", "/")}')
    doc.drawString(375, 175, f'Due Date {due_date.replace("-", "/")}')

def write_summary_header(doc, start_date, end_date):
    doc.setFont('Times-Roman', FONT_XL)
    doc.drawString(75, 255, 'Summary')
    doc.setFont('Times-Roman', FONT_S)
    doc.setFillColor('gray')
    doc.drawString(200, 253.5, f'{start_date.replace("-", "/")} - {end_date.replace("-", "/")}')
    doc.setFillColor('black')
    doc.setFont('Times-Roman', FONT_S)
    doc.setFillColor('gray')
    doc.drawString(75, 280, 'Services')
    doc.drawString(350, 280, 'Quantity')
    doc.drawString(475, 280, 'Amount')
    doc.setFillColor('black')
    draw_hr(doc, 290)

def write_line_item(doc, name, start_date, end_date, quantity, 
                    subtotal, currency_symbol, line_item_start):
    title_offset = line_item_start + 20
    datespan_offset = line_item_start + 27
    doc.setFont('Times-Roman', FONT_S)
    doc.drawString(75, title_offset, name)
    doc.setFillColor('gray')
    doc.setFont('Times-Italic', FONT_XXS)
    doc.drawString(75, line_item_start + 35, f'{start_date.replace("-", "/")} - {end_date.replace("-", "/")}')
    doc.setFont('Times-Roman', FONT_S)
    doc.setFillColor('black')
    doc.drawString(350, datespan_offset, str(quantity))
    doc.drawString(475, datespan_offset, f'{currency_symbol}{str(subtotal)}')
    doc.setFillColor('black')
    draw_hr(doc, line_item_start + 45)
    return line_item_start + 45

def write_total(doc, currency_symbol, total, current_y):
    offset = current_y+ 50
    doc.setFont('Times-Roman', FONT_S)
    doc.drawString(75, offset, 'Toal Due')
    doc.drawString(475, offset, f'{currency_symbol}{total}')

def generate_invoice(invoice_json):
    doc = canvas.Canvas("output.pdf", pagesize=letter, bottomup=0)

    write_invoice_title(doc)
    write_seller_details(doc, invoice_json['seller']['name'], invoice_json['seller']['address']['line1'], 
                              invoice_json['seller']['address']['city'], invoice_json['seller']['address']['state'],
                              invoice_json['seller']['address']['country'], invoice_json['seller']['address']['postal_code'],
                              invoice_json['seller']['phone'], invoice_json['seller']['email'])

    write_customer_details(doc, invoice_json['customer']['customer_name'], invoice_json['customer']['address']['line1'], 
    invoice_json['customer']['address']['city'], invoice_json['customer']['address']['state'],
    invoice_json['customer']['address']['country'], invoice_json['customer']['address']['postal_code'],
    invoice_json['customer']['email'])

    write_invoice_details(doc, invoice_json['invoice_number'], invoice_json['issue_date'], invoice_json['due_date'])
    write_summary_header(doc,  invoice_json['start_date'], invoice_json['end_date'])
    
    line_item_start_y = 290
    for line_item in invoice_json['line_items']:
        line_item_start_y = write_line_item(doc, line_item['name'], line_item['start_date'], line_item['end_date'], 
                        line_item['quantity'], line_item['subtotal'],invoice_json['currency']['symbol'], line_item_start_y)
        if line_item_start_y > 680:
            doc.showPage()
            line_item_start_y = 40
    
    write_total(doc, invoice_json['currency']['symbol'], invoice_json['cost_due'], line_item_start_y)
    doc.save()

    pdf_file = open("output.pdf", "rb")
    pdf_bytes = BytesIO(pdf_file.read())

    # Create a connection to S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id="YOUR_ACCESS_KEY",
        aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",
    )

    # Specify the name of the bucket
    bucket_name = "my-s3-bucket"

    # Upload the PDF file to S3
    s3.upload_fileobj(
        pdf_bytes,
        bucket_name,
        "path/to/save/file.pdf",
        ExtraArgs={"ContentType": "application/pdf"},
    )
    return doc