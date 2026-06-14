from fastapi import FastAPI
from fastapi.routing import APIRoute
from api.routes.user_router import user_router
from api.routes.task_router import task_router
from api.routes.auth_router import auth_router
from api.routes.metrics_route import metrics_router

def custom_generate_unique_id(route: APIRoute):
    return route.name

app = FastAPI(generate_unique_id_function=custom_generate_unique_id)

app.include_router(user_router)
app.include_router(task_router)
app.include_router(auth_router)
app.include_router(metrics_router)