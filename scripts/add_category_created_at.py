import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import engine
import sqlalchemy as sa

with engine.begin() as conn:
    conn.execute(sa.text("ALTER TABLE categories ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))

print('column added')
