from flask import Flask, render_template,request
from main import MLprocessing
app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():

    question=request.args.get('q', "Does Korean stil eat dog?")
    return MLprocessing(question)

if __name__ == "__main__":
    print("==========reload=========")
    print("==========reload=========")
    print("==========reload=========")
    
    app.run(debug=True, host='0.0.0.0', port=9000)
