import smtplib 
import sys
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class mail:
    """This class receives two parameters : a log file and SQL file.
    These files are sent to the destinarion emails when the backup is finished"""

    message_body = f"""
    <div style="height: 100px;
                background-color: rgb(153, 152, 235);
                text-align: center;
                justify-content: center;">
        <h1>Registro DataBase Backup</h1>
        <p>Se envia el registro de la creacion del backup de la base de datos generado {date}</p>
    </div>"""


    def __init__(self,log,sql,emails,credentials):
        """Default constructor
        
        Args :
        log(String) : LOg file
        sql(String) : SQL file
        emails(String) : Emails file
        credentials(String) : Credentials file
        """
        self._logfile = log
        self._sqlfile = sql
        self._credentials_df = pd.read_csv(credentials,sep=",",header=0,skipinitialspace=True)
        self._emails_df = pd.read_csv(emails,sep=",",header=0,skipinitialspace=True)
    
    def run(self):
        """It validates the connection to the SMTP server , sends notification messages
            and attachments to the emails list.
        """
        #Set up the SMTP server
        s = smtplib.SMTP(host='smtp.gmail.com',port=587)
        s.starttls()
        s.login(
            self._credentials_df['email'].iloc[0], 
            self._credentials_df['credential'].iloc[0], #row 0 
        )
        for _, row in self._emails_df.iterrows():
            msg = MIMEMultipart() #Create a message
            # Setup the parameters of the message
            msg['From'] = row['name']
            msg['To'] = row['email']
            msg['Subject'] = "Backup: "+ self._sqlfile

            # Add in the message body
            msg.attach(MIMEText(message_body,'html'))
            self.add(self._logfile,msg)
            self.add(self._sqlfile,msg)

            #Send the message via the server set up earlier
            s.send_message(msg)
            print("Mensaje enviado")
            print(msg)
            del msg
        #Terminate the SMTP session and close the connection
        s.quit()

    def add(self,file,msg):
        """It adds the log and SQL files in the email attachment.
        Args:
            file(String) : File name
            msg(String) : Parameters of the message
        """
        attach = MIMEApplication(open(file).read(),_subtype = "txt")
        attach.add_header('Content-Disposition','attachment',filename=str(os.path.basename(file)))
        msg.attach(attach)
    
if __name__ == '__main__':
    m = mail(
        log = sys.argv[1],
        sql = sys.argv[2],
        emails = sys.argv[3],
        credentials =sys.argv[4]
    )
    m.run()