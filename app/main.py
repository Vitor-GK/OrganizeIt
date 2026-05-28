from fastapi import FastAPI
from fastapi.routing import APIRoute

def custom_generate_unique_id(route: APIRoute):
    return route.name

app = FastAPI(generate_unique_id_function=custom_generate_unique_id)