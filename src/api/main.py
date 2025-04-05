from fastapi import FastAPI
from src.api.pravda.endpoints import router as pravda_router
from src.api.home.endpoints import router as home_router
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
app.include_router(pravda_router)
app.include_router(home_router)


@app.get("/", response_class=HTMLResponse)
def redirect_to_home():
    """
    Redirects to the home page.
    """
    return RedirectResponse(url="/home")
