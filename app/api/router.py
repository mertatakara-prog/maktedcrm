from fastapi import APIRouter

from app.api.routers import activities, customers, task_events, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(customers.router)
api_router.include_router(activities.router)
api_router.include_router(task_events.router)
