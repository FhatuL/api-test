from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import randint

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/random', methods=['GET', 'POST'])
def random():
    if request.method == 'GET':
        cafes = Cafe.query.all()
        i = randint(0, len(cafes)-1)

        cafe = cafes[i]
        return jsonify(name = cafe.name, 
                        map_url = cafe.map_url,
                        img_url = cafe.img_url,
                        location = cafe.location,
                        seats = cafe.seats,
                        has_toilet = cafe.has_toilet,
                        has_wifi = cafe.has_wifi, 
                        has_sockets = cafe.has_sockets,
                        can_take_calls = cafe.can_take_calls,
                        coffee_price = cafe.coffee_price,
                        id = cafe.id  
                        )


@app.route('/all')
def all():
    pass
    cafes = Cafe.query.all()
    all_cafes = []
    for cafe in cafes:
        all_cafes.append(cafe.to_dict())

    return jsonify(all_cafes)

@app.route('/search')   
def search():
    pass
    search = request.args.get('loc').lower().title()
    print(search)

    cafes = Cafe.query.filter_by(location=search).all()


    if len(cafes) == 0:
        return {
            'error': {
                'Not Found': 'Sorry, we don\'t have a cafe at that location'
            }
        }, 404

    return jsonify([cafe.to_dict() for cafe in cafes])

@app.route('/add', methods = ['POST'])
def add():
    data = request.form
    cafe = Cafe(
        name = data['name'],
        map_url = data['map_url'],
        img_url = data['img_url'],
        location = data['location'],
        seats = data['seat'],
        has_toilet = bool(data['has_toilet']),
        has_wifi = bool(data['has_wifi']),
        has_sockets = bool(data['has_sockets']),
        can_take_calls = bool(data['can_take_calls']),
        coffee_price = data['coffee_price']
    )
    db.session.add(cafe)
    db.session.commit()

    return jsonify(response = {'success': 'Successfully added a new cafe.'}), 200
    
@app.route('/update-price/<cafe_id>', methods = ['PATCH'])
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:

        cafe.coffee_price = request.args.get('new_price')
        db.session.commit()

        return jsonify(success = 'Successfully updated the price'), 200
    return jsonify(error = {"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
