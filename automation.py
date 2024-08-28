# db_tool/automation.py
import os

def setup_cron_job(script_path, schedule):
    cron_job = f"{schedule} /bin/bash {script_path} >> db_tool/logs/cron.log 2>&1"
    os.system(f'(crontab -l ; echo "{cron_job}") | sort - | uniq - | crontab -')
    print(f"Cron job set: {cron_job}")

def remove_cron_job(script_path):
    os.system(f'crontab -l | grep -v "{script_path}" | crontab -')
    print(f"Cron job for {script_path} removed")

