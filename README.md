# challenge_email_service
For this challange the django framework has been selected as back-end, where a single django app has been implemented, i.e. mail: https://github.com/yhamacnu/challenge_email_service/tree/main/app/mail

The app is containerized and could be build/run via(.env for providing api keys): docker-compose up [-d]

Dependencies are handled by the requirements.txt file: https://github.com/yhamacnu/challenge_email_service/blob/main/app/requirements.txt

Almost, no effort has been invested/implemented in the frontend: https://github.com/yhamacnu/challenge_email_service/tree/main/app/mail/templates

The request handler is implemented as a view function, that processes the email template form. 
The failover is handled by the https://github.com/yhamacnu/challenge_email_service/blob/main/app/mail/failover.py module, which implements a rudimental responsibility chain mail send handler.
Failover trigger of primary email(SparkPost) provider is simulated by having an account with an non-configured/non-verified sending domain, that reports code 7001 or raises SparkPostAPIException. 
Backup provider is AWS SES.

List of files modified by me:
https://github.com/yhamacnu/challenge_email_service/blob/main/docker-compose.yml
https://github.com/yhamacnu/challenge_email_service/blob/main/app/Dockerfile
https://github.com/yhamacnu/challenge_email_service/blob/main/app/requirements.txt
https://github.com/yhamacnu/challenge_email_service/blob/main/app/email_service/settings.py - minor
https://github.com/yhamacnu/challenge_email_service/blob/main/app/email_service/urls.py - minor
https://github.com/yhamacnu/challenge_email_service/tree/main/app/mail/templates - form templates and html files
https://github.com/yhamacnu/challenge_email_service/blob/main/app/mail/failover.py
https://github.com/yhamacnu/challenge_email_service/blob/main/app/mail/forms.py
https://github.com/yhamacnu/challenge_email_service/blob/main/app/mail/views.py
