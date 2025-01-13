from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
import os

app = Flask(__name__)

# Klasör var mı, yoksa oluştur
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# PDF sıkıştırma fonksiyonu
def compress_pdf(input_path, output_path):
    # PDF dosyasını açıyoruz
    doc = fitz.open(input_path)

    # Her sayfayı sıkıştırma
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Sayfa içeriğini sıkıştırma
        pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))  # 0.5 oranında küçültme
        pix.save(output_path)

    doc.save(output_path)
    return output_path

@app.route('/')
def index():
    return render_template('compress.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        return 'No file part', 400
    pdf_file = request.files['pdf_file']
    
    if pdf_file.filename == '':
        return 'No selected file', 400
    
    # Dosyayı kaydediyoruz (uploads klasörüne)
    input_path = os.path.join('uploads', pdf_file.filename)
    pdf_file.save(input_path)
    
    # Çıkış dosyası adı
    output_path = os.path.join('uploads', f"compressed_{pdf_file.filename}")
    
    # PDF'i sıkıştırıyoruz
    compress_pdf(input_path, output_path)
    
    # Kullanıcıya sıkıştırılmış dosyayı gönderiyoruz
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
