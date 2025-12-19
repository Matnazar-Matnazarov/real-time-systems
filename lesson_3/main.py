from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.message import EmailMessage
from environs import Env

env = Env()
_ = env.read_env()

SMTP_HOST = env.str("SMTP_HOST")
SMTP_PORT = int(env.str("SMTP_PORT", "587"))
SMTP_USER = env.str("SMTP_USER")
SMTP_PASS = env.str("SMTP_PASS")
FROM_NAME = env.str("FROM_NAME", "FastAPI Mailer")
FROM_EMAIL = env.str("FROM_EMAIL", SMTP_USER)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def send_email_smtp(to_email: str, subject: str, body: str):
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS]):
        raise RuntimeError("SMTP sozlamalari topilmadi. .env faylni tekshiring.")

    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # TLS bilan ulanish
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        _ = smtp.ehlo() 
        if SMTP_PORT in (587, 25):
            _ = smtp.starttls()
            _ = smtp.ehlo()
        _ = smtp.login(SMTP_USER, SMTP_PASS)
        _ = smtp.send_message(msg)


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send", response_class=HTMLResponse)
async def send(
    request: Request,
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    message: str = Form(...),
    subject: str = Form("Xabar FastAPI dan"),
):
    try:
        valid_email_info = validate_email(email)
        valid_email = valid_email_info.email
    except EmailNotValidError:
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "ok": False, "msg": "Email noto'g'ri kiritildi."},
            status_code=400,
        )

    try:
        background_tasks.add_task(send_email_smtp, valid_email, subject, message)
    except Exception as e:
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "ok": False, "msg": f"Xatolik: {e}"},
            status_code=500,
        )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "ok": True,
            "msg": "Xabar yuborish jo'natildi — tekshiring inbox/kirish papkasini.",
        },
    )
