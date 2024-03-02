from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'sec_oixDgaiu41gif64dTAXyYgaZaw3XscVS'  

# Helper function to send a message and return the response
def send_message_to_bot(data):
    headers = {
        "x-api-key": "sec_oixDgaiu41gif64dTAXyYgaZaw3XscVS",
        "Content-Type": "application/json",
    }
    url = "https://api.chatpdf.com/v1/chats/message"
    
    response = requests.post(url, json=data, headers=headers, stream=True)
    response.raise_for_status()

    return response.text

@app.route('/')
def index():
    return render_template('send_message_form.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     file = request.files['file']
    
#     if file.filename == '':
#         return 'No selected file'
    
#     files = {'file': ('file.pdf', file.stream, 'application/octet-stream')}
#     headers = {'x-api-key': 'sec_oixDgaiu41gif64dTAXyYgaZaw3XscVS'}  
#     response = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
    
#     if response.status_code == 200:
#         source_id = response.json()['sourceId']
#         session['source_id'] = source_id  # Store sourceId in session
#         return redirect('/send-message')  
#     else:
#         return f'Error: {response.status_code} - {response.text}'

@app.route('/send-message', methods=['GET','POST'])
def send_message():
    if 'source_id' not in session:
        return 'Source ID not found in session'
    
    source_id = 'src_NmoU5zgj6y9eYn8iPxUa8' # Retrieve sourceId from session
    
    if request.method == 'POST':
        user_message = request.form['user_message']
        data = {
            "stream": True,
            "sourceId": source_id, 
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        }
        
        bot_response = send_message_to_bot(data)
        return render_template('send_message_response.html', response_text=bot_response)
    
    # Render the form without sending any initial message
    return render_template('send_message_form.html')

if __name__ == '__main__':
    app.run(debug=True)
