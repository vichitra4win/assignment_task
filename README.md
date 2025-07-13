
# RBCApp1 Monitoring & Data Processing Project

This repository contains three key tasks:

1. **Test1** – A Python-based monitoring and REST API service for `rbcapp1`.
2. **Test2** – Ansible-based automation to verify service installation, check disk usage, and assess application health.
3. **CSV Filtering Task** – A Python script that filters real estate records below average price per square foot.

---

## Contents

```
.
├── monitor-service.py                  # Python service monitoring script
├── app.py                      # Flask REST API for Elasticsearch integration
├── playbook.yml                # Ansible playbook for system automation
├── inventory                   # Ansible inventory for multi-host monitoring
├── filter.py                   # CSV filter script for real estate data
├── output.csv                  # Output CSV from filter.py
├── README.md                   # This documentation
└── Commands & screenshots.docs # command reference and screenshot proof
```

---

## Test1: Python Monitoring + REST API + Elasticsearch

### Prerequisites

- Python 3.x
- pip3
- Elasticsearch 7.x
- Apache2, RabbitMQ, PostgreSQL
- Virtualenv

### Setup

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
python3 -m venv ~/rbcapp-monitoring-env
source ~/rbcapp-monitoring-env/bin/activate
pip install flask elasticsearch requests
```

### Install Required Services

```bash
sudo apt install -y apache2 rabbitmq-server postgresql
```

### Install and Start Elasticsearch

```bash
sudo apt install -y openjdk-17-jdk apt-transport-https
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update && sudo apt install -y elasticsearch
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
curl http://localhost:9200
```

### Step 1: Monitor Services

```bash
python3 monitor.py
# This creates individual JSON files per service with status
```

### Step 2: Run Flask REST API

```bash
python3 app.py
# Endpoints available at http://localhost:5000
```

### Step 3: API Endpoints

- `POST /add`: Upload service JSON file to Elasticsearch
- `GET /healthcheck`: Return overall app status (UP/DOWN)
- `GET /healthcheck/<service>`: Status of a specific service

Example:

```bash
curl -X POST http://localhost:5000/add -F "file=@apache2-status-20250713-145513.json"
curl http://localhost:5000/healthcheck
curl http://localhost:5000/healthcheck/apache2
```

---

## Test2: Ansible Playbook Automation

### Prerequisites

```bash
sudo apt install -y ansible
ansible-galaxy collection install community.general
```

### Inventory File Example (`inventory`)

```ini
[httpd]
host1 ansible_host=IP

[rabbitmq]
host2 ansible_host=IP

[postgresql]
host3 ansible_host=IP

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### Supported Actions

#### 1. `verify_install`

Checks and installs missing services. Example (for Ubuntu):

```yaml
- name: Ensure Apache2 is installed
  apt:
    name: apache2
    state: present
    update_cache: yes
```

```bash
ansible-playbook playbook.yml -i inventory -e action=verify_install
```

#### 2. `check-disk`
```yaml
  - name: Check for disk partitions over 80% usage
    shell: |
      df -h --output=pcent,target | tail -n +2 | tr -d '%' | awk '$1 > 80 {print $0}'
    register: disk_alert
```
## Email Alerts with Gmail

Ensure the `check-disk` playbook section uses Gmail SMTP:

```yaml
community.general.mail:
  host: smtp.gmail.com
  port: 587
  username: "your_email@gmail.com"
  password: "your_app_password"
  to: "your_email@gmail.com"
  subject: "Disk Alert"
  body: "Disk usage on {{ inventory_hostname }} is critical."
  secure: starttls
```

Use App Passwords (not your Gmail login). Generate here: https://myaccount.google.com/apppasswords
we can pass the password as argument, variable or we can encrypt the playbook using vault for the security.

```bash
ansible-playbook playbook.yml -i inventory -e action=check-disk
```

Uses Gmail App Password with `community.general.mail` module.

#### 3. `check-status`

Calls the REST API and checks app status:

```bash
ansible-playbook playbook.yml -i inventory -e action=check-status
```

---

## Task: Filter Real Estate Data by Price/Sqft

### Description

This task filters properties whose **price per square foot is less than the average**.

### Setup & Run

```bash
pip install pandas
python3 filter.py
```

### Output

- Input file: `sales-data.csv`
- Output file: `ouput.csv`

---


## Sample Commands Summary


```bash
python3 monitor.py                       # Monitor service status to JSON
python3 app.py                           # Run Flask API
curl -X POST http://localhost:5000/add -F "file=@status.json"
ansible-playbook playbook.yml -e action=check-disk
python3 filter.py                        # CSV filter logic
```


