from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips.db'
db = SQLAlchemy(app)

class IP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reversed_ip = db.Column(db.String(15), nullable=False)


@app.route('/')
def display_ip():
    # Get client IP
    ip = request.remote_addr
    # Reverse the IP
    reversed_ip = '.'.join(ip.split('.')[::-1])
    # Store the reversed IP in the database
    new_ip = IP(reversed_ip=reversed_ip)
    db.session.add(new_ip)
    db.session.commit()
    # Render the HTML template with the IP and reversed IP
    return render_template('index.html', ip=ip, reversed_ip=reversed_ip)

@app.route('/all')
def display_all():
    # Query all reversed IPs from the database
    ips = IP.query.all()
    # Convert the results to a list of reversed IPs
    reversed_ips = [ip.reversed_ip for ip in ips]
    # Render a template with the list of reversed IPs
    return render_template('all.html', reversed_ips=reversed_ips)

@app.route('/')
def hello_world():
    ip = request.remote_addr
    reversed_ip = '.'.join(ip.split('.')[::-1])
    new_ip = IP(reversed_ip=reversed_ip)
    db.session.add(new_ip)
    db.session.commit()
    return 'Hello, your reversed IP is: %s\n' % reversed_ip

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=5001)
