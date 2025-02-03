from flask import Flask, render_template, request, redirect, url_for, jsonify
import model
import vectorstore

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(f'uploads/{file.filename}')  # Save the file
        return redirect(url_for('home'))
    return render_template('upload.html')



@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    response = model.gen_response(user_input)
    bot_reply = response.text
    return jsonify({"reply": bot_reply})

@app.route('/vectorize', methods=['GET'])
def vectorize():
    vectorstore.main()
    return jsonify({"status": "success", "message": "Vectorization Completed"})
if __name__ == '__main__':
    app.run(debug=True)
