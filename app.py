from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
db = SQLAlchemy(app)

# Models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)       # "Bobby pins"
    category = db.Column(db.String(50))                    # "Wigs"
    unit = db.Column(db.String(50))                        # "pcs"
    count = db.Column(db.Integer, default=0)
    desc = db.Column(db.Text)
    low_stock_threshold = db.Column(db.Integer, default=5)
    logs = db.relationship('CountLog', backref='item', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'unit': self.unit,
            'count': self.count,
            'desc': self.desc,
            'is_low': self.count <= self.low_stock_threshold
        }

class CountLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    delta = db.Column(db.Integer, nullable=False)          # +1 or -3 etc.
    count_after = db.Column(db.Integer, nullable=False)    # count after this change
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(200))                       # optional, "restocked before event"

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'delta': self.delta,
            'count_after': self.count_after,
            'timestamp': self.timestamp.isoformat(),
            'note': self.note
        }

with app.app_context():
    db.create_all()     # create database if not yet existing

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)