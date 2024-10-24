from fastapi import FastAPI
from routers import analyze_and_summarize

app = FastAPI()

app.include_router(analyze_and_summarize.router)