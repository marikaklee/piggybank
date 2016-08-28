from flask import Flask, render_template, request, session, redirect, url_for
from config import PUBLIC_KEY, PRIVATE_KEY
import simplify
from datetime import datetime, time
import time
import datetime
import json
import pandas as pd

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/", methods=['GET'])
def home():
    # If you're not logged in, go back to login page
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')

    if 'invoice' in session.keys():
        if session['invoice'] == '':
            return render_template('home.html')
        else:
            return render_template('home.html', invoice=session['invoice'])
    else:
        return render_template('home.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return redirect(url_for("home"))
    else:
        return render_template('login.html')

@app.route("/logout", methods=['GET'])
def logout():
    session['username'] = ''
    return render_template('login.html')


@app.route("/payment")
def payment_home():
    # If you're not logged in, go back to login page
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    session['invoice'] = ''
    return render_template("payment.html",key=PUBLIC_KEY)

@app.route("/makePayment",methods=["POST"])
def payment():

    simplify.public_key = PUBLIC_KEY
    simplify.private_key = PRIVATE_KEY

    payment = simplify.Payment.create({
        "token" : token,
        "amount" : "1000",
        "description" : "Example on How to use",
        "currency" : "USD"
    })

    session["status"] = payment.paymentStatus
    session["id"] = payment.authCode
    session["amount"] = payment.amount

    print session['id']
    print session['amount']
    print token

    if payment.paymentStatus == 'APPROVED':
        return redirect(url_for("paymentSuccess"))
    else:
        return "Payment not approved"

@app.route("/paymentsuccess")
def paymentSuccess():
    amount = session["amount"]/100
    return render_template("payment_success.html",amount=amount,id=session["id"])


@app.route('/invoice', methods=['GET'])
def invoice_home():
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    session['invoice'] = ''
    return render_template("invoice.html", key=PUBLIC_KEY)

@app.route('/makeInvoice', methods=['POST'])
def invoice():
    memo = request.form["memo"]
    email = request.form["email"]
    amount = request.form["amount"]

    dueDate = str(int(time.time()) + (24 * 60 * 60 * int(request.form["dueDate"])))
   
    dateCreated = str(int(time.time()))

    simplify.public_key = PUBLIC_KEY
    simplify.private_key = PRIVATE_KEY

    invoice = simplify.Invoice.create({
        "memo" : memo,
        "items" : [
           {
              "amount" : amount,
              "quantity" : "1"
           }
        ],
        "email" : email,
        "name" : "Customer",
        "dateCreated" : dateCreated,
        "dueDate" : dueDate,
        "reference" : "Ref2",
        "currency" : "USD"
    }) 
 
    print invoice
    session['invoice'] = invoice.id
    return redirect(url_for('home'))


if __name__=="__main__":
    app.run("0.0.0.0",5000)
