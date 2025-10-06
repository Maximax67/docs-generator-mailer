from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional

from app.email import render_reset_password_email, send_email, render_confirm_email
from app.settings import settings


app = FastAPI(title=settings.APP_TITLE)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    to_email: str
    subject: str
    template: str
    username: str
    url: str


def verify_token(x_api_token: Optional[str]) -> None:
    if x_api_token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Token")


@app.get("/")
async def status(request: Request, response: Response) -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/send-email")
async def send_email_endpoint(
    request: EmailRequest, response: Response, x_api_token: Optional[str] = Header(None)
) -> Dict[str, str]:
    verify_token(x_api_token)

    if request.template == "confirm":
        html_content = render_confirm_email(request.username, request.url)
    elif request.template == "reset":
        html_content = render_reset_password_email(request.username, request.url)
    else:
        raise HTTPException(status_code=400, detail="Invalid template type")

    await send_email(request.to_email, request.subject, html_content)

    return {"message": "Email sent successfully"}
