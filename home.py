from flask import Flask, render_template, redirect, request
from flask_basicauth import BasicAuth
import requests
import os
import configparser

app = Flask(__name__)

# Configure Basic Authentication
app.config['BASIC_AUTH_USERNAME'] = 'ouss'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
basic_auth = BasicAuth(app)

#############################
# Helper Functions          #
#############################

def fail2ban_status():
    """Check the status of the Fail2ban service."""
    status = os.popen('service fail2ban status').read()
    if "inactive" in status or "not running" in status:
        return "Fail2ban is not running"
    elif "active" in status or "is running" in status:
        return "Fail2ban is running"

def read_config(file_path):
    """Read and return the configuration from the specified file."""
    cp = configparser.RawConfigParser()
    cp.read(file_path)
    return cp

def get_country(ip):
    """Retrieve country information for a given IP address."""
    response = requests.get(f'http://ip-api.com/json/{ip}')
    return response.json()

#############################
# Routes                    #
#############################

@app.route('/')
@basic_auth.required
def redirect_to_home():
    return redirect('/home', code=302)

@app.route('/home', methods=['GET', 'POST'])
@basic_auth.required
def home():
    status = fail2ban_status()
    return render_template('index.html', status=status)

@app.route('/start', methods=['POST'])
def start_fail2ban():
    os.popen('service fail2ban start')
    return redirect("/", code=302)

@app.route('/stop', methods=['POST'])
def stop_fail2ban():
    os.popen('service fail2ban stop')
    return redirect("/", code=302)

@app.route('/config', methods=['GET', 'POST'])
@basic_auth.required
def config():
    config_file = '/etc/fail2ban/jail.conf'
    cp = read_config(config_file)
    services = cp.sections()
    return render_template('config.html', cp=cp, services=services)

@app.route('/enable/<service>', methods=['POST'])
def enable_service(service):
    config_file = '/etc/fail2ban/jail.conf'
    cp = read_config(config_file)
    cp.set(service, 'enabled', 'true')
    with open(config_file, 'w') as configfile:
        cp.write(configfile)
    os.popen('service fail2ban restart')
    return redirect("/config", code=302)

@app.route('/disable/<service>', methods=['POST'])
def disable_service(service):
    config_file = '/etc/fail2ban/jail.conf'
    cp = read_config(config_file)
    cp.set(service, 'enabled', 'false')
    with open(config_file, 'w') as configfile:
        cp.write(configfile)
    os.popen('service fail2ban restart')
    return redirect("/config", code=302)

@app.route('/display/<filter>', methods=['GET', 'POST'])
@basic_auth.required
def display_filter(filter):
    try:
        file_path = f"/etc/fail2ban/filter.d/{filter}.conf"
        with open(file_path, 'r') as file:
            filter_content = file.read()
    except IOError:
        filter_content = "There is a problem with this filter."
    return render_template('filter.html', filter_content=filter_content, service=filter)

@app.route('/save/<filter>', methods=['POST'])
def save_filter(filter):
    try:
        filter_content = request.form['filter']
        file_path = f"/etc/fail2ban/filter.d/{filter}.conf"
        with open(file_path, 'w') as file:
            file.write(filter_content)
    except IOError:
        return render_template('filter.html', filter_content="There is a problem with this filter.")
    return redirect('/config', code=302)

@app.route('/banned', methods=['GET', 'POST'])
@basic_auth.required
def banned():
    banned_ips = []
    with open('/var/log/fail2ban.log', 'r') as log_file:
        for line in log_file:
            if 'Ban' in line:
                banned_ips.append(line)
    return render_template('banned.html', banned_ips=banned_ips, get_country=get_country)

#############################
# App Launcher              #
#############################

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
