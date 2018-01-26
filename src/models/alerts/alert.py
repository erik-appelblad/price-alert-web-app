import datetime
import uuid
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None,_id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Alert for {} on item {} with price {}".format(self.user_email, self.item, self.price_limit)

    def send_alert_email(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "We've found a deal {link}"
            }
        )

    def save_to_db(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active":self.active
        }

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})

    def activate(self):
        self.active = True
        self.save_to_db()

    def deactivate(self):
        self.active = False
        self.save_to_db()

    def send_email_if_limit_reached(self):
        try:
            if float(self.item.price) < float(self.price_limit):
                self.send_alert_email()
        except ValueError as e:
            print(e)

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_db()
        self.save_to_db()
        return self.item.price

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                        {"$lte": last_updated_limit},
                                                       "active": True
                                                      })]

    @classmethod
    def find_by_user_email(cls, email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user_email": email})]

    @classmethod
    def find_by_id(cls, id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": id}))
