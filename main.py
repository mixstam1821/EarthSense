from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from bokeh.embed import server_document
import uvicorn

app = FastAPI(title="EarthSense")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "active_page": "home"}
    )
@app.get("/intro", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        "intro.html",
        {"request": request, "active_page": "intro"}
    )

@app.get("/app1_mirror", response_class=HTMLResponse)
async def app1(request: Request):
    script = server_document("http://localhost:9798/bokeh_apps/app1_mirror")#http://localhost:5006/bokeh_apps/scatter_app
    return templates.TemplateResponse(
        "bokeh_app.html",
        {"request": request, "script": script, "active_page": "app1_mirror", "title": "EarthSense3"}
    )

@app.get("/app2_mirror", response_class=HTMLResponse)
async def app2(request: Request):
    script = server_document("http://localhost:9798/bokeh_apps/app2_mirror")
    return templates.TemplateResponse(
        "bokeh_app.html",
        {"request": request, "script": script, "active_page": "app2_mirror", "title": "EarthSense1"}
    )

@app.get("/app3_mirror", response_class=HTMLResponse)
async def app3(request: Request):
    script = server_document("http://localhost:9798/bokeh_apps/app3_mirror")
    return templates.TemplateResponse(
        "bokeh_app.html",
        {"request": request, "script": script, "active_page": "app3_mirror", "title": "EarthSense2"}
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "active_page": "about"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9797, reload=True)
