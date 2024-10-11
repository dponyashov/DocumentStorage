import os
from dataclasses import dataclass

@dataclass(frozen=True)
class _Config:
    DB_URL = os.environ.get('DB_URL', 'sqlite:///db_dir/docstorage.db')