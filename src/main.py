from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from fastapi import FastAPI

from src.controllers.item_controller import item_router
from contextlib import asynccontextmanager
from src.controllers.auth_controller import auth_router


def my_daily_task():
    print(f"Task is running at {datetime.now()}")


# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(minute="*")
scheduler.add_job(my_daily_task, trigger)
scheduler.start()

load_dotenv()


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(prefix="/api/items", router=item_router)
app.include_router(prefix="/api/users", router=auth_router)
