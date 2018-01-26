from flask import Blueprint, render_template, request, session, redirect, url_for

from src.models.alerts.alert import Alert
from src.models.items.item import Item
from src.models.users.decorators import requires_login

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return "this is alerts index"


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        try:
            price_limit = float(request.form['price_limit'])
        except ValueError:
            price_limit = 0.0
        item = Item(name, url)
        item.save_to_db()
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()  # also saves to mongodb, good design?
        return redirect(url_for("users.user_alerts"))

    return render_template("alerts/create_alert.html")


@alert_blueprint.route('/deactivate/<string:alert_id>')
@requires_login
def deactivate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.deactivate()
    return redirect(url_for(".get_alert_page", alert_id=alert_id))

@alert_blueprint.route('/activate/<string:alert_id>')
@requires_login
def activate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.activate()
    return redirect(url_for(".get_alert_page", alert_id=alert_id))

@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.delete()
    return redirect(url_for("users.user_alerts"))

@alert_blueprint.route('/<string:alert_id>')
@requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template("alerts/alert.html", alert=alert)

@alert_blueprint.route('/check_price/<string:alert_id>')
@requires_login
def check_price(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.load_item_price()
    return redirect(url_for(".get_alert_page", alert_id=alert_id))
