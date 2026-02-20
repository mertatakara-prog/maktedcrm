from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.router import api_router
from app.core.config import settings
from app.db.session import get_db

app = FastAPI(title=settings.app_name)
app.include_router(api_router)


@app.get('/health', tags=['health'])
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text('SELECT 1'))
    return {'status': 'ok'}
