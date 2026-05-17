from fastapi import FastAPI

from src.routers import location_r, category_r, user_r, comment_r, post_r


app = FastAPI()

app.include_router(location_r.router)
app.include_router(category_r.router)
app.include_router(user_r.router)
app.include_router(comment_r.router)
app.include_router(post_r.router)
