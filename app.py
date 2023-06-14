import os
import logging
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('RDS_USERNAME')}:{os.getenv('RDS_PASSWORD')}@je-deel.cpl9h4c99kwt.us-east-2.rds.amazonaws.com:5432/je-deel"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.wsgi_app = ProxyFix(app.wsgi_app)  # To get the correct IP behind a proxy (like Nginx)

db = SQLAlchemy(app)

class IP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reversed_ip = db.Column(db.String(15), nullable=False)

@app.route('/')
def display_ip():
    try:
        ip = request.remote_addr
        reversed_ip = '.'.join(ip.split('.')[::-1])
        existing_ip = IP.query.filter_by(reversed_ip=reversed_ip).first()
        if not existing_ip:
            new_ip = IP(reversed_ip=reversed_ip)
            db.session.add(new_ip)
            db.session.commit()
        return render_template('index.html', ip=ip, reversed_ip=reversed_ip)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return render_template('error.html'), 500

@app.route('/all')
def display_all():
    try:
        ips = IP.query.all()
        reversed_ips = [ip.reversed_ip for ip in ips]
        return render_template('all.html', reversed_ips=reversed_ips)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return render_template('error.html'), 500

@app.route('/health')
def health_check():
    try:
        # Run a simple SELECT query
        result = db.engine.execute('SELECT 1')
        # If the query was successful, return a positive response
        if result.fetchone()[0] == 1:
            return 'Database connection successful', 200
    except Exception as e:
        # If there was an error, log it and return a negative response
        app.logger.error(f"Database connection failed: {e}")
        return 'Database connection failed', 500

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=5001)
