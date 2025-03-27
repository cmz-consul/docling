# from flask import Flask, request, send_file, render_template
# from docling.document_converter import DocumentConverter
# import os
# import json
# import io
# import requests
# from requests.exceptions import SSLError, RequestException

# app = Flask(__name__, static_folder='static', template_folder='static')

# os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/convert', methods=['POST'])
# def convert_pdf():
#     output_format = request.form.get('format', 'markdown')
#     temp_path = os.path.join(os.path.dirname(__file__), "temp.pdf")

#     if 'pdfFile' in request.files and request.files['pdfFile']:
#         pdf_file = request.files['pdfFile']
#         pdf_file.save(temp_path)
#     elif 'pdfUrl' in request.form and request.form['pdfUrl']:
#         pdf_url = request.form['pdfUrl']
#         try:
#             # Tenta baixar o PDF, ignorando verificação SSL como fallback
#             response = requests.get(pdf_url, verify=False, timeout=10)
#             if response.status_code != 200:
#                 return f"Erro ao baixar o PDF da URL: Status {response.status_code}", 400
#             with open(temp_path, 'wb') as f:
#                 f.write(response.content)
#         except SSLError:
#             return "Erro de SSL ao baixar o PDF. A URL pode ter um certificado inválido ou protocolo não suportado.", 400
#         except RequestException as e:
#             return f"Erro ao acessar a URL: {str(e)}", 400
#     else:
#         return "Nenhum arquivo ou URL fornecido", 400

#     converter = DocumentConverter()
#     result = converter.convert(temp_path)

#     if output_format.lower() == "json":
#         output_data = result.document.export_to_dict()
#         output_buffer = io.BytesIO(json.dumps(output_data, ensure_ascii=False, indent=4).encode('utf-8'))
#         mimetype = 'application/json'
#         filename = 'converted_file.json'
#     else:
#         output_data = result.document.export_to_markdown()
#         output_buffer = io.BytesIO(output_data.encode('utf-8'))
#         mimetype = 'text/markdown'
#         filename = 'converted_file.md'

#     if os.path.exists(temp_path):
#         os.remove(temp_path)

#     output_buffer.seek(0)
#     return send_file(output_buffer, mimetype=mimetype, as_attachment=True, download_name=filename)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)




from flask import Flask, request, send_file, render_template
from docling.document_converter import DocumentConverter
import os
import json
import io
import requests
from requests.exceptions import RequestException
import urllib3

# Suprime avisos de requisições HTTPS inseguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__, static_folder='static', template_folder='static')

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    output_format = request.form.get('format', 'markdown')
    temp_path = os.path.join(os.path.dirname(__file__), "temp.pdf")

    if 'pdfFile' in request.files and request.files['pdfFile']:
        pdf_file = request.files['pdfFile']
        pdf_file.save(temp_path)
    elif 'pdfUrl' in request.form and request.form['pdfUrl']:
        pdf_url = request.form['pdfUrl']
        try:
            # Faz a requisição ignorando SSL e suprimindo avisos
            response = requests.get(pdf_url, verify=False, timeout=10)
            if response.status_code != 200:
                return f"Erro ao baixar o PDF da URL: Status {response.status_code}", 400
            with open(temp_path, 'wb') as f:
                f.write(response.content)
        except RequestException as e:
            return f"Erro ao acessar a URL: {str(e)}", 400
    else:
        return "Nenhum arquivo ou URL fornecido", 400

    converter = DocumentConverter()
    result = converter.convert(temp_path)

    if output_format.lower() == "json":
        output_data = result.document.export_to_dict()
        output_buffer = io.BytesIO(json.dumps(output_data, ensure_ascii=False, indent=4).encode('utf-8'))
        mimetype = 'application/json'
        filename = 'converted_file.json'
    else:
        output_data = result.document.export_to_markdown()
        output_buffer = io.BytesIO(output_data.encode('utf-8'))
        mimetype = 'text/markdown'
        filename = 'converted_file.md'

    if os.path.exists(temp_path):
        os.remove(temp_path)

    output_buffer.seek(0)
    return send_file(output_buffer, mimetype=mimetype, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)