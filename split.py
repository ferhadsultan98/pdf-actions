from flask import Flask, render_template, request, send_file
import PyPDF2
from io import BytesIO

app = Flask(__name__)

# Ana sayfa için route
@app.route('/')
def index():
    return render_template('split.html')  # HTML dosyasını templates/ klasöründen render eder

@app.route('/split_pdf', methods=['POST'])
def split_pdf():
    start_page = int(request.form['start']) - 1  # 0-indexed
    end_page = int(request.form['end']) - 1  # 0-indexed
    pdf_file = request.files['pdf']

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(start_page, end_page + 1):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    # PDF dosyasını bellek üzerinde oluştur
    output_pdf = BytesIO()
    pdf_writer.write(output_pdf)
    output_pdf.seek(0)

    return send_file(output_pdf, as_attachment=True, download_name="split_pdf.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
