import requests
import smtplib # for email
import os # for getting environment variables
import paramiko # for ssh
import linode_api4 # for linode
import time
import schedule

# assign environment variable to a variable(constant) in python
EMAIL_ADD = os.environ.get('EMAIL_ADDRESS') # best practice to write a constant in uppercase
EMAIL_PWD = os.environ.get('EMAIL_PASSWORD')
# the environment variables can be assigned in the editor itself
# can either provide the actual gmail password, or create a specific 'app' password just for this use case.
LINODE_API_TOKEN = os.environ.get('LINODE_API_TOKEN')


def send_email(email_message):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:  # assigning smptlib.SMTP"" etc. to smtp
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADD, EMAIL_PWD)  # login with environment variables
        # send email with parameters: sender, recipient, and the email message:
        message = f"Subject: SITE DOWN\n {email_message}"
        smtp.sendmail(EMAIL_ADD, EMAIL_ADD, message)

def restart_container():
    print('Restarting the Application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # to make it non-interactive ssh
    ssh.connect(hostname='172.236.20.248', username='root', key_filename='/Users/ausman/.ssh/id_rsa')
    # provided private key location instead of password. remote server already contains the public key
    stdin, stdout, stderr = ssh.exec_command('docker start b8a2dbe4df51 ')
    print(stdout.readlines())
    ssh.close()
    print('Application restarted')


def restart_server_and_container():
    # restart linode server. commands specific to linode. Use documentation to know what commands to use.
    print('Rebooting the server...')
    client = linode_api4.LinodeClient(LINODE_API_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 73652578)
    nginx_server.reboot()

    # restart application
    while True:
        nginx_server = client.load(linode_api4.Instance, 73652578)
        if nginx_server.status == 'running':  # wait for server to start running before restarting container
            time.sleep(5)
            restart_container()
            break

def monitor_application():
    try:
        response = requests.get('http://172.236.20.248:8080')
        if response.status_code == 200:
            print('Application is Running')
        else:
            print('Application is down')
            # send email to me
            msg = f"Application returned {response.status_code}"
            send_email(msg)

            # restart the application
            restart_container()
    except Exception as ex:
        print(f"Connection is down: {ex}")
        msg = f"Application is not even reachable"
        send_email(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()






