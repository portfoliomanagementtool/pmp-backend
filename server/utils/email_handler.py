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
  <head>
    <meta charset="utf-8" />
    <title>Portfolio Invoice</title>

    <style>
     {}
    </style>
  </head>

  <body>
    <div class="invoice-box">
      <table cellpadding="0" cellspacing="0">
        <tr class="top">
          <td colspan="2">
            <table>
              <tr>
                <td class="title">
                  Portfolio
                </td>

                <td>
                  
                  Date:{}
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr class="heading">
          <td>Description</td>

          <td>Value</td>
        </tr>

        <tr class="item">
          <td>Invested Value</td>

          <td>${}</td>
        </tr>

        <tr class="item">
          <td>Market Value</td>

          <td>${}</td>
        </tr>

        <tr class="item last">
          <td>Overall Profit Loss</td>

          <td>${}</td>
        </tr>

      </table>
	  <tr class="information">
		<td colspan="2">
			<table>
				<tr>
					<td class="checkout-link">
						Checkout Your Portfolio <span><a href="https://portfolio-management-platform.netlify.app/app/dashboard">Here</a></span><br />
					</td>

				</tr>
			</table>
		</td>
	</tr>

    </div>
  </body>
</html>
        """.format(
            """
 .invoice-box {
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
        font-size: 16px;
        line-height: 24px;
        font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
        color: #555;
      }

      .invoice-box table {
        width: 100%;
        line-height: inherit;
        text-align: left;
      }

      .invoice-box table td {
        padding: 5px;
        vertical-align: top;
      }

      .invoice-box table tr td:nth-child(2) {
        text-align: right;
      }

      .invoice-box table tr.top table td {
        padding-bottom: 20px;
      }

      .invoice-box table tr.top table td.title {
        font-size: 45px;
        line-height: 45px;
        color: #333;
      }

      .invoice-box table tr.information table td {
        padding-bottom: 40px;
      }

      .invoice-box table tr.heading td {
        background: #eee;
        border-bottom: 1px solid #ddd;
        font-weight: bold;
      }

      .invoice-box table tr.details td {
        padding-bottom: 20px;
      }

      .invoice-box table tr.item td {
        border-bottom: 1px solid #eee;
      }

      .invoice-box table tr.item.last td {
        border-bottom: none;
      }

      .invoice-box table tr.total td:nth-child(2) {
        border-top: 2px solid #eee;
        font-weight: bold;
      }

	  .checkout-link{
		font-weight: medium;
		color: #333;
	  }

      @media only screen and (max-width: 600px) {
        .invoice-box table tr.top table td {
          width: 100%;
          display: block;
          text-align: center;
        }

        .invoice-box table tr.information table td {
          width: 100%;
          display: block;
          text-align: center;
        }
      }

      /** RTL **/
      .invoice-box.rtl {
        direction: rtl;
        font-family: Tahoma, "Helvetica Neue", "Helvetica", Helvetica, Arial,
          sans-serif;
      }

      .invoice-box.rtl table {
        text-align: right;
      }

      .invoice-box.rtl table tr td:nth-child(2) {
        text-align: left;
      }
""",
            datetime.datetime.now().strftime("%Y-%m-%d"),round(invested_value,2),round(market_value,2),round(overall_pl,2))
        #Send email on background Thread
        x=Process(target=send_email, args=("Portfolio Overview", body, [recipient]))
        x.daemon=True
        x.start()
    except Exception as e:
        print(f"Error in formatting: {e}")
