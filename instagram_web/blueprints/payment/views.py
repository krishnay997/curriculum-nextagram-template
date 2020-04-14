from flask import Flask,Blueprint, render_template,redirect,request,url_for,flash,session

from models.user import User,Images,Amount
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
import os
import braintree
import requests

payment_blueprint = Blueprint('payment',
                            __name__,
                            template_folder='templates')

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("BT_MERCHANT_ID"),
        public_key=os.environ.get("BT_PUBLIC_KEY"),
        private_key=os.environ.get("BT_PRIVATE_KEY")
    )
)



@payment_blueprint.route("/<image_id>")
@login_required
def new(image_id):
    client_token=gateway.client_token.generate()
    return render_template("payment/payment.html", client_token=client_token,image_id=image_id)

@payment_blueprint.route("/checkout", methods=["POST"])
@login_required
def checkout():
    print(request.form)
    result = gateway.transaction.sale({
        "amount": request.form["amount"],
        "payment_method_nonce": request.form["payment_method_nonce"],
        "options": {
            "submit_for_settlement": True
        }
    })

    first_amount=request.form.get("amount")
    real_amount=int(first_amount)*100
    image_url=Images.get_or_none(Images.id==request.form.get("image_id"))
    receiver=User.get_or_none(User.id==image_url.user_id)
    am=Amount(amount_donated=real_amount,donator_username=current_user.username,recipient_username=receiver.username,image_url=image_url.image_path)
    am.save()
    print(result)
    send_message()
    return 'ok bro'

def send_message():
    image_url=Images.get_or_none(Images.id==request.form.get("image_id"))
    receiver=User.get_or_none(User.id==image_url.user_id)
    print("***********************************************************************")
    print(receiver.email)
    print(type(receiver.email))
    print("***********************************************************************")
    return requests.post(
        "https://api.mailgun.net/v3/"+os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": "Excited User <mailgun@"+os.environ.get("MAILGUN_DOMAIN")+">",
              "to": [f"{receiver.email}"],
              "subject": "Hellozzz",
              "text": "Works bro"})