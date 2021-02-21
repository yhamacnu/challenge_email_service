# challenge_email_service
For this challange the django framework has been selected as back-end, where a single django app has been implemented, i.e. mail: https://github.com/yhamacnu/challenge_email_service/tree/main/app/mail

The app is containerized and could be build/run via(.env for providing api keys): docker-compose up [-d]

Dependencies are handled by the requirements.txt file: https://github.com/yhamacnu/challenge_email_service/blob/main/app/requirements.txt

Almost, no effort has been invested/implemented in the frontend: https://github.com/yhamacnu/challenge_email_service/tree/main/app/mail/templates

The request handler is implemented as a view function, that processes the email template form. Ther rudimentary failover is also handled there.
Fail trigger of primary email(SparkPost) provider is simulated by having an account with an non-configured/non-verified sending domain, that reports code 7001 and raises SparkPostAPIException. 
Backup provider is AWS SES.
