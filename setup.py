from pathlib import Path
from Config import LoggingConfig, AppConfig
import logging
import json

log_path = Path(AppConfig.App.LOG_PATH)
log_path.mkdir(exist_ok=True)
active_log_file = log_path / (AppConfig.App.APP_NAME + ".log")
error_log_file = log_path / (AppConfig.App.APP_NAME + "Error.log")
LoggingConfig.configure_logging(str(active_log_file), str(error_log_file))
logging.info("log_path is " + str(log_path.resolve()))

tmp_path = AppConfig.App.TMP_PATH
tmp_path.mkdir(exist_ok=True)
logging.info("tmp_path is " + str(tmp_path.resolve()))

done_files_path = AppConfig.App.TMP_PATH / "done_files.json"
if not done_files_path.exists():
    with open(done_files_path, "w") as done_files_f_r:
        json.dump([], done_files_f_r)
playlist_path = AppConfig.App.PLAYLIST_PATH