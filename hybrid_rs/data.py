import gdown
from loguru import logger


def download(file_id, output_path):
    url = f'https://drive.google.com/uc?id={file_id}'

    logger.info(f"Скачивание {output_path}...")
    gdown.download(url, output_path, quiet=False)
    logger.info(f"Скачивание {output_path} завершено.")
