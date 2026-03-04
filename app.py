from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/inventory.db'
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

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)