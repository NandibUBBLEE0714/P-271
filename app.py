import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from twilio.rest import Client


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login' , methods=['POST'])
def verify_otp():
    username = request.form['username']
    password = request.form['password']
    mobile_number = request.form['number']

    if username == 'verify' and password == '12345':   
        account_sid = 'AC4f4da881e0c8bac7448399648ab9f0fe'
        auth_token = '26ab2702c609f3510d39cc33792f1a29'
        client = Client(account_sid, auth_token)

        verification = client.verify \
            .services('VA34202927429ab62d9134c926278a2da9') \
            .verifications \
            .create(to=mobile_number, channel='sms')

        print(verification.status)
        return render_template('otp_verify.html')
    else:
        return render_template('user_error.html')



@app.route('/otp', methods=['POST'])
def get_otp():
    print('processing')

    received_otp = request.form['received_otp']
    mobile_number = request.form['number']

    account_sid = 'AC4f4da881e0c8bac7448399648ab9f0fe'
    auth_token = '26ab2702c609f3510d39cc33792f1a29'
    client = Client(account_sid, auth_token)
                                            
    verification_check = client.verify \
        .services('VA34202927429ab62d9134c926278a2da9') \
        .verification_checks \
        .create(to=mobile_number, code=received_otp)
    print(verification_check.status)

    if verification_check.status == "pending":
        return render_template('otp_error.html')
    else:
        return redirect("https://collaborative-notepad-65wr.onrender.com/")


if __name__ == "__main__":
    app.run()

