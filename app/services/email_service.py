import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from core.config import settings

# Configuración SMTP
SMTP_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "username": settings.smtp_user,
    "password": settings.smtp_pass,
    "use_tls": True,
}

# Configuración de plantillas
TEMPLATES_DIR = "email_templates"
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def send_email_template(to_email: str, subject: str, template_name: str, **template_data) -> bool:
    """Envía un correo basado en una plantilla HTML."""
    try:
        # Cargar y renderizar la plantilla
        template = env.get_template(template_name)
        html_content = template.render(**template_data)

        # Construcción del correo
        msg = MIMEMultipart()
        msg["From"] = SMTP_CONFIG["username"]
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        # Envío del correo
        with smtplib.SMTP(SMTP_CONFIG["host"], SMTP_CONFIG["port"]) as server:
            if SMTP_CONFIG["use_tls"]:
                server.starttls()
            server.login(SMTP_CONFIG["username"], SMTP_CONFIG["password"])
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

def send_contact_email(name: str, email: str, message: str, subject: str) -> bool:
    """Envía un correo de contacto."""
    return send_email_template(email, subject, "contact-us.html", name=name, message=message)

def send_recovery_email(email: str, plain_password: str) -> bool:
    """Envía un correo con la contraseña temporal."""
    return send_email_template(email, "Tu contraseña temporal está lista", "recovery-email.html", password=plain_password)
