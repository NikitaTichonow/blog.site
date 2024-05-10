import os
from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomStorage(FileSystemStorage):
    """Пользовательское хранилище для изображений."""
    date = datetime.now().strftime('%Y/%m/%d')
    location = os.path.join(settings.MEDIA_ROOT, f"post/{date}/")
    base_url = urljoin(settings.MEDIA_URL, f"post/{date}/")