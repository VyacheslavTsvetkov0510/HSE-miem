from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import os

DEFAULT_DATABASE_URI = 'mysql+pymysql://root:password@localhost/count_db'

app = Flask(__name__)

# Parse environment variables
for variable, value in os.environ.items():
    app.config[variable] = value

# Set up logging
app.logger.setLevel(logging.DEBUG)

# Connect to database
uri = DEFAULT_DATABASE_URI
if all(k in app.config.keys() for k in ['DATABASE_USER', 'DATABASE_PASSWORD', 'DATABASE_HOST', 'DATABASE_NAME']):
    uri = f"mysql+pymysql://{app.config['DATABASE_USER']}:{app.config['DATABASE_PASSWORD']}@{app.config['DATABASE_HOST']}"
    if 'DATABASE_PORT' in app.config.keys():
        uri += str(app.config['DATABASE_PORT'])
    uri+= f"/{app.config['DATABASE_NAME']}"
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

class ProcessedNumber(db.Model):
    num = db.Column(db.Integer, primary_key=True)

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return 'Proccessed number %r' % self.num

def is_valid_number(n):
    # Input should contain digits only
    if any(not c.isdigit() for c in str(n)):
        return False
    # Check if it converts to int
    try:
        int(n)
    except ValueError:
        return False
    return True

@app.route('/increase', methods=['POST'])
def increase():
    # Validate request data
    if not request.is_json:
        return jsonify({'error' : 'Expected json'}), 400
    data = request.get_json()
    if not 'num' in data:
        return jsonify({'error' : 'Expected "num" in request body' }), 400
    if not is_valid_number(data['num']):
        return jsonify({'error' : 'Expected "num" to be a natural number'}), 400
    
    num = int(data['num'])

    res = ()

    # num is NOT in database
    if ProcessedNumber.query.filter_by(num=num).first() is None:
        # num+1 is NOT in database
        if ProcessedNumber.query.filter_by(num=num+1).first() is None:
            res = (jsonify({'increased_num' : num+1}), 200)
        # num+1 is in database
        else:
            app.logger.info(f'User {request.remote_addr} sent number {num}. {num} + 1 is found in database')
            res = (jsonify({'error' : str(num) + '+1 exists in database'}), 409)
        try:
            # add num to database 
            new_num = ProcessedNumber(num)
            db.session.add(new_num)
            db.session.commit()
        except SQLAlchemyError as e:
            app.logger.error(str(e.__dict__['orig']))        
            res = (jsonify({'error' : 'Application server error'}),500)
    # num is in database
    else:
        app.logger.info(f'User {request.remote_addr} sent number {num}. This number is found in database')
        res = (jsonify({'error' : str(num) + ' exists in database'}), 409)
    
    return res

if __name__ == '__main__':
    app.run(debug=True)



