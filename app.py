from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    files = {'file': ('file.pdf', file.stream, 'application/octet-stream')}
    headers = {'x-api-key': 'sec_oixDgaiu41gif64dTAXyYgaZaw3XscVS'}  # Replace 'sec_xxxxxx' with your actual API key
    
    response = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
    
    if response.status_code == 200:
        source_id = response.json()['sourceId']
        return f'File uploaded successfully. Source ID: {source_id}'
    else:
        return f'Error: {response.status_code} - {response.text}'

if __name__ == '__main__':
    app.run(debug=True)
