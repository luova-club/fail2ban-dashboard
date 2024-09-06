# Fail2ban Dashboard

[![Build Status](https://travis-ci.org/luova-club/fail2ban-dashboard.svg?branch=master)](https://travis-ci.org/luova-club/fail2ban-dashboard)

A sleek web dashboard for Fail2ban, built with Flask, to offer enhanced visibility and control over your security.

## Overview

Fail2ban Dashboard is a web application developed with Flask to help monitor and manage Fail2ban on your server. Initially created in 2015 as a learning project for Python and Flask, it has since evolved to offer more robust features and improved usability.

## Quick Start

### Clone the Repository

```bash
$ git clone https://github.com/luova-club/fail2ban-dashboard.git
$ cd fail2ban-dashboard
```

### Set Up the Environment

Create and activate a virtual environment:

```bash
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

Install the required dependencies:

```bash
$ pip install -r requirements.txt
```

### Run the Development Server

```bash
$ python home.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

**Login:** `ouss`  
**Password:** `pass`

## Deployment

For a more production-ready setup, deploy the application using Gunicorn:

```bash
$ pip install gunicorn
$ gunicorn home:app -p fail2ban_dashboard.pid -b 0.0.0.0:5000 -D
```

## Contributing

The project is actively under development. We welcome contributions, feedback, and suggestions. Feel free to open an [issue](https://github.com/luova-club/fail2ban-dashboard/issues) or contribute directly to the codebase.

## System Requirements

Developed and tested on Debian Wheezy. Ensure compatibility with your environment.

## Screenshots

- **Home Dashboard:**

  ![Home](docs/screenshots/home.png)

- **Configuration:**

  ![Config](docs/screenshots/config.png)

- **Filter Configuration:**

  ![Config filter](docs/screenshots/configure_filter.PNG)

- **Banned IP Details:**

  ![Banned IP](docs/screenshots/get_country1.PNG)

## Changelog

- **(28-10-2014)**: Introduced filter configuration and password authentication.
- **(21-09-2015)**: Added compatibility with init and systemd. Thanks to [@nocternology](https://github.com/nocternology).
- **(30-03-2016)**: Integrated IP geolocation via [ip-api.com](http://ip-api.com/json/).

## Bonus

- **(15-11-2014)**: Available as a Docker container preconfigured with Debian Wheezy.

  ```bash
  $ docker pull oussemos/fail2ban-dashboard
  ```

## Author

Developed by Verso.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
