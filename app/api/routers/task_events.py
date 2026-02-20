from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task_event import TaskEvent
from app.schemas.task_event import TaskEventCreate, TaskEventRead

router = APIRouter(prefix='/task-events', tags=['task_events'])


@router.post('', response_model=TaskEventRead, status_code=201)
def create_task_event(payload: TaskEventCreate, db: Session = Depends(get_db)) -> TaskEvent:
    task_event = TaskEvent(**payload.model_dump())
    db.add(task_event)
    db.commit()
    db.refresh(task_event)
    return task_event


@router.get('', response_model=list[TaskEventRead])
def list_task_events(db: Session = Depends(get_db)) -> list[TaskEvent]:
    return db.query(TaskEvent).order_by(TaskEvent.id.asc()).all()
