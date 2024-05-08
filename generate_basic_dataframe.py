import io
import logging
import os

import pandas as pd
from docx import Document
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import authenticate_drive

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CACHE_FILE = "caches/dataframe_cache.pkl"
SJC_FOLDER_ID = "1Y4vQAMnKFZDc8xVzSmjROqzjx9oo3gPS"
CREDENTIALS = authenticate_drive.authenticate()
SERVICE = build("drive", "v3", credentials=CREDENTIALS)


def get_week_folders() -> list[dict]:
    logger.info("Getting week folders...")
    query = f"'{SJC_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = (
        SERVICE.files().list(q=query, fields="files(name, id)", pageSize=100).execute()
    )
    weeks = results.get("files", [])
    return weeks


def get_submissions_from_week_folder(week_folder_id: str) -> list[dict]:
    logger.info(f"Getting submissions from week folder {week_folder_id}...")
    query = f"'{week_folder_id}' in parents and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')"
    results = (
        SERVICE.files()
        .list(q=query, fields="files(name, id, owners, mimeType, createdTime)", pageSize=100)
        .execute()
    )
    entries = results.get("files", [])
    return entries


def get_docx_file_contents(file_id: str) -> str:
    logger.info(f"Downloading docx file content for file {file_id}...")
    request = SERVICE.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        logger.info(f"Download {int(status.progress() * 100)}%.")
    fh.seek(0)
    doc = Document(fh)
    content = " ".join([paragraph.text for paragraph in doc.paragraphs])
    logger.info(f"Download completed :)")
    return content


def get_google_doc_file_contents(file_id: str) -> str:
    logger.info(f"Downloading file content for file {file_id}...")
    fh = io.BytesIO()
    request = SERVICE.files().export_media(fileId=file_id, mimeType="text/plain")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        logger.info(f"Download {int(status.progress() * 100)}%.")
    fh.seek(0)
    content = fh.read().decode()
    logger.info(f"Download completed :)")
    return content


def generate_basic_dataframe(use_cache: bool = True) -> pd.DataFrame:
    logger.info("Generating basic dataframe...")
    logger.info(f"use_cache: {use_cache}")
    if os.path.exists(CACHE_FILE) and use_cache:
        logger.info("Loading cached dataframe...")
        df = pd.read_pickle(CACHE_FILE)
    else:
        df = pd.DataFrame(columns=["week", "title", "content", "author", "file_id", "upload_date"])

    week_folders = get_week_folders()
    for week_folder in week_folders:
        submissions = get_submissions_from_week_folder(week_folder["id"])
        for submission in submissions:
            # cache check
            if submission["id"] in df["file_id"].values:
                logger.info(
                    f"Cached file {submission['id']} skipping download..."
                )
                continue

            week = week_folder["name"]
            title = submission["name"]
            author = submission["owners"][0]["emailAddress"]
            upload_date = submission["createdTime"]
            content = ""

            if (
                submission["mimeType"]
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                content = get_docx_file_contents(submission["id"])
            elif submission["mimeType"] == "application/vnd.google-apps.document":
                content = content = get_google_doc_file_contents(submission["id"])
            else:
                logger.error(f"Unknown file type {submission['mimeType']} for file {title}, week {week}. Skipping entry...")
                continue

            file_id = submission["id"]

            new_row = {
                "week": week,
                "title": title,
                "content": content,
                "author": author,
                "file_id": file_id,
                "upload_date": upload_date,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_pickle(CACHE_FILE)

    return df
