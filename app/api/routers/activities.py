from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityRead

router = APIRouter(prefix='/activities', tags=['activities'])


@router.post('', response_model=ActivityRead, status_code=201)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_db)) -> Activity:
    activity = Activity(**payload.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.get('', response_model=list[ActivityRead])
def list_activities(db: Session = Depends(get_db)) -> list[Activity]:
    return db.query(Activity).order_by(Activity.id.asc()).all()
