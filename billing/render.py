import os
import pdfkit
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


# Invoice Rendering
class InvoiceFile:
    path = os.path.abspath('billing/static/billing/invoices/')
    html_path = os.path.join(path, 'html')
    pdf_path = os.path.join(path, 'pdf')
    template_path = "billing/invoice.html"

    # Generate HTML
    def generate_html(self, invoice):
        context = {'invoice': invoice}
        file = render_to_string(self.template_path, context)
        output = os.path.join(self.html_path, invoice.invoice_no + '.html')
        with open(output, 'w+') as output_html:
            output_html.write(file)
        return output

    # Convert HTML to Pdf
    def convert_pdf(self, file):
        name = os.path.basename(file)
        out_name = name.replace('.html', '.pdf')
        output = os.path.join(self.pdf_path, out_name)
        pdfkit.from_file(file, output)
        return output

    # Get Invoice Path
    def get_pdf(self, number):
        for f in os.listdir(self.pdf_path):
            if os.path.splitext(os.path.basename(f))[0] == number:
                pdf = os.path.join(self.pdf_path, f)
                return pdf
            else:
                raise FileNotFoundError

    # Generate
    def generate(self, invoice):
        out_html = self.generate_html(invoice)
        out_pdf = self.convert_pdf(out_html)
        return out_pdf

    # Send Invoice as receipt
    def send_receipt(self, target):
        # Prepare email
        sender = settings.EMAIL_HOST_USER
        subject = target['subject']
        body = target['body']
        receiver = target['receiver']
        invoice_no = self.get_pdf(target['invoice'])
        pdf = open(invoice_no, 'rb')
        # Send email
        msg = EmailMessage(subject, body, sender, [receiver])
        msg.attach('invoice.pdf', pdf.read(), 'application/pdf')
        msg.send()
