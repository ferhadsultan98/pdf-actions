from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger
import io

app = Flask(__name__)

# Anasayfa (HTML sayfasını render et)
@app.route('/')
def index():
    return render_template('merge.html')  # HTML dosyasını templates/ klasöründen render eder

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    # Yüklenen dosyalar
    files = request.files.getlist('pdfs')
    merger = PdfMerger()

    # Dosyaları bellekte işleyip birleştiriyoruz
    for file in files:
        merger.append(io.BytesIO(file.read()))  # File'ı okur ve bellekteki BytesIO objesine ekler

    # Birleştirilmiş PDF'yi belleğe yazıyoruz
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    merged_pdf.seek(0)  # Okuma pozisyonunu başa al

    # Birleştirilmiş PDF'yi kullanıcıya gönderiyoruz
    return send_file(merged_pdf, as_attachment=True, download_name="merged.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
