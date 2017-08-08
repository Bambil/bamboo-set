from flask import Flask, render_template, request
import requests
import os


app = Flask(__name__)


@app.route('/')
def calc():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getnum():
    text = request.form['textarea']
    num = text.split()
    ipadd = os.environ['add_ip']
    ipsub = os.environ['sub_ip']
    ipmul = os.environ['mul_ip']
    ipdiv = os.environ['div_ip']

    if num[1]=="+" :
        r = requests.post('http://' + ipadd + ':3000/add',json={"param1": num[0],"param2" : num[2]})
    if num[1]=="-" :
        r = requests.post('http://' + ipsub + ':3000/sub',json={"param1": num[0],"param2" : num[2]})
    if num[1]=="*" :
        r = requests.post('http://' + ipmul + ':3000/mul',json={"param1": num[0],"param2" : num[2]})
    if num[1]=="/" :
        r = requests.post('http://' + ipdiv + ':3000/div',json={"param1": num[0],"param2" : num[2]})
    return r.text


if __name__ == "__main__":
    app.run(host='0.0.0.0')