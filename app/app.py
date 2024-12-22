from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Добавлено для подавления предупреждения
db = SQLAlchemy(app)

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))

@app.route('/partners', methods=['POST'])
def add_partner():
    data = request.get_json()
    new_partner = Partner(name=data['name'], email=data['email'])
    db.session.add(new_partner)
    db.session.commit()
    return jsonify({'message': 'New partner added!'})

@app.route('/materials', methods=['POST'])
def add_material():
    data = request.get_json()
    new_material = Material(title=data['title'], description=data['description'], partner_id=data['partner_id'])
    db.session.add(new_material)
    db.session.commit()
    return jsonify({'message': 'New material added!'})

@app.route('/materials', methods=['GET'])
def get_materials():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    materials = Material.query.paginate(page, per_page, error_out=False)
    return jsonify({
        'materials': [material.to_dict() for material in materials.items],
        'total': materials.total,
        'pages': materials.pages,
        'current_page': materials.page
    })

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
