from fastapi import FastAPI

from src.routers import category_r, comment_r, location_r, post_r, user_r, auth_r

app = FastAPI()

app.include_router(auth_r.router)
app.include_router(location_r.router)
app.include_router(category_r.router)
app.include_router(user_r.router)
app.include_router(comment_r.router)
app.include_router(post_r.router)
