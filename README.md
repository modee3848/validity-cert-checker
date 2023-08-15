# validity-cert-checker
Simple script to use in cron to check validity of remote and local certificates

This script was developed to create a simple tool for monitoring the validity of certificates - both local and remote, with a notification system. The goal of the project was to create a tool that allows for easy and convenient certificate validity checking and will notify the administrator of their expiration or any other irregularities, thereby relieving and automating the tasks required to check certificates. The script was primarily designed for the Linux system with the possibility of automation using the Cron program. Our notification system is based on the mechanism of sending emails through an SMTP server to the inbox of the interested user. The program is executed by invoking the appropriate command in the console.

For local cert example:
sudo python3 LocalCert.py ./creds.txt testuser@test.com

The program requires superuser privileges - only they have access to the files where we check the certificates. The first argument we need is the path to the file containing our SMTP server login data, which we will use to send email messages. The second argument is the target email address where we want to receive the message.

Executing for remote cert:
python3 RemoteCert.py ./creds.txt ./test.txt testuser@test.com

The first argument we need is the path to the file containing our login data for the SMTP server, which we will use to send email messages. The second argument is the path to the file where we have listed the services we are interested in 
Example format for file with services
wit.pwr.edu.pl:443
zsmilicz.eu:443
jsos.pwr.edu.pl:443
wp.pl:443
The last argument is the target email address where we want to receive the message.

