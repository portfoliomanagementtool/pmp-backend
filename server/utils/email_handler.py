import smtplib
from email.mime.text import MIMEText
import os
import environ
from multiprocessing import Process
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
sender=env("EMAIL_ID")
password = env("EMAIL_PASSWORD")



def send_email(subject, body, recipients):
    try:
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
            print("Message sent!")
    except Exception as e:
        print(f"Error: {e}")
def send_portfolio_email_template(recipient, invested_value, market_value, overall_pl):
    try:
        import datetime
        body="""
        <html>
        <head></head>
        <body>
        <h1>Portfolio Overview</h1>
        <p>Invested Value: ${}</p>
        <p>Market Value: ${}</p>
        <p>Overall PL: ${}</p>
        <p>Date: {}</p>
        <p>Check Your Portfolio <a href="https://portfolio-management-platform.netlify.app/app/dashboard">Here</a></p>
        <p>Regards,<br>Portfolio Manager</p>
        </body>

        </html>
        """.format(round(invested_value,2),round(market_value,2),round(overall_pl,2),datetime.datetime.now().strftime("%Y-%m-%d"))
        #Send email on background Thread
        x=Process(target=send_email, args=("Portfolio Overview", body, [recipient]))
        x.daemon=True
        x.start()
    except Exception as e:
        print(f"Error: {e}")
