import os
import pdfkit
from django.shortcuts import render
from django.template.loader import render_to_string


# Invoice Rendering
class InvoicePdf:
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
