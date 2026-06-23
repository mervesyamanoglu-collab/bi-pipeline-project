# 4_pipeline_orchestrator.py

import subprocess
import smtplib
import os
import logging
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = os.getenv("SENDER_EMAIL")
SMTP_PASSWORD = os.getenv("SENDER_PASSWORD")
EMAIL_TO      = os.getenv("RECEIVER_EMAIL")

logging.basicConfig(
    filename="pipeline_log.txt",
    level=logging.INFO,
    format="%(asctime)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

scripts = [
    "1_data_collection.py",
    "2_data_cleaning.py",
    "2b_forecast_transform.py",
    "3_data_storage.py",
    "5_machine_learning.py",
]

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"]    = SMTP_USER
        msg["To"]      = EMAIL_TO
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"  [EMAIL SENT] {subject}")
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        print(f"  [EMAIL FAILED] {e}")
        logging.error(f"Email failed: {e}")

def run_pipeline():
    print("=" * 55)
    print(f"  PIPELINE START — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)
    logging.info("Pipeline started")

    failed_steps = []

    for script in scripts:
        print(f"\n  Running: {script}")
        result = subprocess.run(
            ["python", script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if result.stdout:
            print(result.stdout.strip())

        stdout_has_error = "ERROR:" in result.stderr

        if result.returncode != 0 or stdout_has_error:
            print(f"  [FAILED] {script}")
            if result.stderr:
                print(result.stderr.strip())
            failed_steps.append(script)
            logging.error(f"FAILED: {script} | {result.stderr.strip()}")
            send_email(
                subject=f"[BI-PIPELINE] FAILED: {script}",
                body=(
                    f"A pipeline step has failed.\n\n"
                    f"Script:    {script}\n"
                    f"Time:      {datetime.now()}\n\n"
                    f"Output:\n{result.stdout}\n\n"
                    f"Error:\n{result.stderr}"
                )
            )
        else:
            print(f"  [SUCCESS] {script}")
            logging.info(f"SUCCESS: {script}")

    print("\n" + "=" * 55)
    if failed_steps:
        print(f"  PIPELINE FINISHED WITH ERRORS: {failed_steps}")
        logging.warning(f"Pipeline finished with errors: {failed_steps}")
    else:
        print("  PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 55)
        logging.info("Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()