import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(docs_url=None, redoc_url=None)  # disable docs in prod
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Support comma-separated origins so localhost works in dev alongside prod
_raw_origins = os.environ.get("ALLOWED_ORIGINS", os.environ.get("ALLOWED_ORIGIN", ""))
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

SMTP_HOST     = os.environ["SMTP_HOST"]
SMTP_PORT     = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER     = os.environ["SMTP_USER"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
TO_EMAIL      = os.environ["TO_EMAIL"]


class ContactForm(BaseModel):
    name:     str = Field(..., min_length=1, max_length=100)
    email:    EmailStr
    subject:  str = Field(default="", max_length=200)
    message:  str = Field(..., min_length=10, max_length=2000)
    honeypot: str = Field(default="", max_length=100)


@app.post("/contact")
@limiter.limit("3/minute")
async def contact(request: Request, form: ContactForm):
    if form.honeypot:
        # Bot filled the hidden field — lie and return success
        logger.warning("Honeypot triggered from %s", get_remote_address(request))
        return {"ok": True}

    try:
        msg = MIMEMultipart()
        msg["Subject"] = f"[Portfolio] {form.subject or 'New message'} — from {form.name}"
        msg["From"]    = SMTP_USER
        msg["To"]      = TO_EMAIL
        msg["Reply-To"] = str(form.email)

        body = (
            f"Name:    {form.name}\n"
            f"Email:   {form.email}\n"
            f"Subject: {form.subject or '(none)'}\n\n"
            f"{form.message}"
        )
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())

        logger.info("Contact form sent from %s", form.email)
        return {"ok": True}

    except Exception as exc:
        logger.error("Failed to send contact email: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to send message. Please try again.")
