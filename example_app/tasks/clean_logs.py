import os

import dramatiq
from django.conf import settings
from periodiq import cron


# Clean logs every 15 days
@dramatiq.actor(periodic=cron("0 0 */15 * *"), max_retries=5)
def clean_logs() -> None:
    try:
        log_dir = settings.LOGGING_DIR
        log_files = [
            f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))
        ]

        for log_file in log_files:
            log_file_path = os.path.join(log_dir, log_file)
            with open(log_file_path, "w") as f:
                f.truncate()
    except Exception:
        raise dramatiq.Retry()
