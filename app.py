from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'sec_oixDgaiu41gif64dTAXyYgaZaw3XscVS'  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    files = {'file': ('file.pdf', file.stream, 'application/octet-stream')}
    headers = {'x-api-key': 'sec_oixDgaiu41gif64dTAXyYgaZaw3XscVS'}  
    response = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
    
    if response.status_code == 200:
        source_id = response.json()['sourceId']
        session['source_id'] = source_id  # Store sourceId in session
        return redirect('/send-message')  
    else:
        return f'Error: {response.status_code} - {response.text}'

@app.route('/send-message', methods=['GET','POST'])
def send_message():
    if 'source_id' not in session:
        return 'Source ID not found in session'
    
    source_id = session['source_id']  # Retrieve sourceId from session
    
    headers = {
        "x-api-key": "sec_oixDgaiu41gif64dTAXyYgaZaw3XscVS",
        "Content-Type": "application/json",
    }

    data = {
        "stream": True,
        "sourceId": source_id, 
        "messages": [
            {
                "role": "user",
                "content": "give a summarized report of this pdf with potential QA and key topics. Provide video link of the video. Please keep the response more human like and give output in points ",  # Get message from form data
            },
        ],
    }

    url = "https://api.chatpdf.com/v1/chats/message"

    try:
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()

        if response.status_code == 200:
            return render_template('send_message_response.html', response_text=response.text)
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as error:
        return f"Error: {error}"

if __name__ == '__main__':
    app.run(debug=True)
