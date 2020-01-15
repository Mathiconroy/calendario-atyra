from django.test import TestCase

from datetime import date, timedelta

# Create your tests here.
class EmailTest(TestCase):
    def sendTestMail(self):
        test_form_results = {'nombre':'Mathias Martinez', 'fecha_inicio':date.today(), 'fecha_fin':date.today() + timedelta(days=1)}
        casa = 'Ysypo Roga'
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = 'mathias.martinez018@gmail.com'
        msgRoot['To'] = form_results['email']
        msgRoot['Subject'] = 'AtyRoga - Reserva hecha'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('Buenas, Mathias.\n We are testing!')
        msgAlternative.attach(msgText)

        msgText = MIMEText(render_to_string('calendarios/mail_test_template.html', context={'form':test_form_results, 'casa':casa}), 'html')
        msgAlternative.attach(msgText)
        
        logo_path = finders.find('calendarios/AtyRoga_Logo.png')
        imgFile = open(logo_path, 'rb')
        msgImage = MIMEImage(imgFile.read())
        imgFile.close()

        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('mathias.martinez018@gmail.com', 'AsdfOwoOmg123456')
        smtp.sendmail('mathias.martinez018@gmail.com', form_results['email'], msgRoot.as_string())
        smtp.quit()