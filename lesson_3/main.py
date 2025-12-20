from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.message import EmailMessage
from environs import Env
import os

env = Env()
# .env faylni o'qish (mavjud bo'lsa)
env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    env.read_env(env_file)
else:
    # .env fayl mavjud emas, default qiymatlar ishlatiladi
    pass

# Environment variables (default qiymatlar bilan)
SMTP_HOST = env.str("SMTP_HOST", default="")
SMTP_PORT = int(env.str("SMTP_PORT", "587"))
SMTP_USER = env.str("SMTP_USER", default="")
SMTP_PASS = env.str("SMTP_PASS", default="")
FROM_NAME = env.str("FROM_NAME", "FastAPI Mailer")
FROM_EMAIL = env.str("FROM_EMAIL", SMTP_USER if SMTP_USER else "")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def send_email_smtp(to_email: str, subject: str, body: str):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        raise RuntimeError(
            "SMTP sozlamalari topilmadi. .env faylni yarating va quyidagilarni to'ldiring:\n"
            "SMTP_HOST=smtp.gmail.com\n"
            "SMTP_PORT=587\n"
            "SMTP_USER=your_email@gmail.com\n"
            "SMTP_PASS=your_app_password\n"
            "FROM_NAME=FastAPI Mailer\n"
            "FROM_EMAIL=your_email@gmail.com"
        )

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


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 FastAPI Email Sender Server")
    print("=" * 60)
    print("📍 Server: http://localhost:8000")
    print("📧 Email yuborish uchun: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        print("\n⚠️  Eslatma: .env fayl topilmadi yoki to'liq emas!")
        print("📝 Email yuborish ishlamaydi. .env.example faylini ko'rib chiqing.")
        print("   Yoki quyidagi o'zgaruvchilarni to'ldiring:")
        print("   - SMTP_HOST")
        print("   - SMTP_USER")
        print("   - SMTP_PASS")
        print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
