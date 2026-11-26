from app.content.config import get_content_backend, get_s3_settings
from app.content.readers import NewsReader, VideoReader
from app.content.s3_client import get_s3_client
from app.news.s3_store import S3NewsStore
from app.news.store import FileNewsStore
from app.videos.s3_store import S3VideoStore
from app.videos.store import FileVideoStore


def select_news_store(local_store: FileNewsStore) -> NewsReader:
    if get_content_backend() == "local":
        return local_store

    bucket, news_key, _ = get_s3_settings()
    return S3NewsStore(get_s3_client(), bucket, news_key)


def select_video_store(local_store: FileVideoStore) -> VideoReader:
    if get_content_backend() == "local":
        return local_store

    bucket, _, video_key = get_s3_settings()
    return S3VideoStore(get_s3_client(), bucket, video_key)