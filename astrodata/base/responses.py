import os
from pathlib import Path
from wsgiref.util import FileWrapper

from django.http import HttpResponseNotFound, StreamingHttpResponse

CHUNK_SIZE = int(os.getenv('DOWNLOAD_CHUNK_SIZE', 1 << 12))


def download_file_response(target_file: Path) -> StreamingHttpResponse:
    if not target_file.exists():
        raise HttpResponseNotFound(f'Unable to find {target_file.name} file.')

    content = FileWrapper(target_file.open("rb"), CHUNK_SIZE)
    return StreamingHttpResponse(content, content_type='application/x-hdf5', headers={
        'Content-Length': target_file.stat().st_size,
        'Content-Disposition': f'attachment; filename={target_file.name}'
    })
