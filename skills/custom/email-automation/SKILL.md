---
name: email-automation
description: Send emails via Gmail, track opens/clicks, templates. Use when you need to send notifications, reports, or automated emails to customers.
---

# Email Automation

## Send Email (Gmail)

```python
import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = 'your@gmail.com'
    msg['To'] = to
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as srv:
        srv.login('your@gmail.com', 'app-password')
        srv.sendmail(msg['From'], msg['To'], msg.as_string())
```

## HTML Email

```python
html = """<html><body>
<h1>New Product Added</h1>
<p>A new item has been added to your wishlist!</p>
</body></html>"""
msg.attach(MIMEText(html, 'html'))
```

## Templates

```python
def render_template(template, **kwargs):
    for k, v in kwargs.items():
        template = template.replace(f'{{{k}}}', str(v))
    return template
```

## SendGrid Alternative

```bash
pip install sendgrid
```

```python
from sendgrid import SendGridAPIClient
sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
sg.send(msg)
```

## Best Practices

- Track opens with tracking pixel
- Use app passwords for Gmail
- Keep emails short
- Include unsubscribe link