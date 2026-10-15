import smtplib
import os
import asyncio
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr, formatdate, make_msgid


try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    load_dotenv(BASE_DIR / ".env")
    load_dotenv(BASE_DIR.parent / ".env")
except ImportError:
    pass

async def send_welcome_verification_email(to_email: str, first_name: str, code: str):
    """Отправка письма с кодом с кодированием заголовков по стандарту Mail.ru"""
    smtp_host = os.getenv("SMTP_HOST", "smtp.mail.ru")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_pass = os.getenv("SMTP_PASS", "").strip()

    subject_str = f"Код подтверждения регистрации {code} — Школа.MAX"

    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="background-color: #030408; font-family: Arial, sans-serif; color: #ffffff; padding: 20px;">
  <div style="max-width: 520px; margin: 0 auto; background: #0c0f1d; border: 1px solid rgba(63, 120, 255, 0.4); border-radius: 20px; padding: 30px;">
    <h2 style="color: #18b5ea; margin-top: 0; text-align: center;">Школа.MAX · Сферум</h2>
    <p style="font-size: 16px; color: #e2e8f0;">Здравствуйте, <b>{first_name}</b>!</p>
    <p style="font-size: 14px; color: #9bb7ff; line-height: 1.5;">
      Ваш адрес <b>{to_email}</b> указан при регистрации в экосистеме Школа.MAX.
    </p>
    <div style="background: linear-gradient(135deg, rgba(24, 181, 234, 0.15), rgba(118, 69, 255, 0.2)); border: 1px solid rgba(63, 120, 255, 0.5); padding: 20px; border-radius: 14px; margin: 24px 0; text-align: center;">
      <span style="font-size: 12px; color: #a2abcb; display: block; margin-bottom: 8px; text-transform: uppercase;">Ваш код подтверждения:</span>
      <b style="font-size: 38px; letter-spacing: 8px; color: #ffffff;">{code}</b>
    </div>
    <p style="font-size: 12px; color: #6e778d; text-align: center;">
      Введите этот код на сайте для подтверждения владения почтой.
    </p>
  </div>
</body>
</html>"""

    def _send_sync():
        if not smtp_user or not smtp_pass:
            print(f"\n⚠️ [ВНИМАНИЕ] SMTP_USER / SMTP_PASS не заполнены в .env!")
            print(f"🔑 КОД ДЛЯ {to_email}: {code}\n")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg.set_charset("utf-8")

          
            msg["Subject"] = Header(subject_str, "utf-8").encode()
            
            
            sender_title = Header("Школа.MAX", "utf-8").encode()
            msg["From"] = formataddr((sender_title, smtp_user))
            msg["To"] = to_email
            
            
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain=smtp_user.split("@")[-1] if "@" in smtp_user else "mail.ru")

            msg.attach(MIMEText(html_content, "html", "utf-8"))

            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=12) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, [to_email], msg.as_string())
            print(f"✅ [SMTP Mail.ru] Письмо с кодом {code} успешно доставлено на {to_email}!")
            return True
        except Exception as e:
            print(f"❌ [SMTP Ошибка] {e}")
            print(f"🔑 КОД ДЛЯ {to_email} (Fallback в консоль): {code}")
            return False

    await asyncio.to_thread(_send_sync)