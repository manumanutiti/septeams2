from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from functions import SepTeam
from info_text import *

# Configuración inicial de FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
sep = SepTeam()


@app.get("/", response_class=HTMLResponse)
def get_graph_page(request: Request, graph_type: str = Query("last_survey")):
    info = ""
    if graph_type == "global":
        global_evaluations = sep.global_mean()
        graph_html = sep.graph(evaluations=global_evaluations, title="All Time View")
        info = info_global
    elif graph_type == "tw_evolution":
        graph_html = sep.tw_evolution()
        info = info_team_work_evolution
    elif graph_type == "hs_evolution":
        graph_html = sep.hs_evolution()
        info = info_hard_skill_evolution
    elif graph_type == "last_survey":
        last_survey = sep.last_survey()
        graph_html = sep.graph(evaluations=last_survey, title="Last Survey")
        info = info_last_survey
    return templates.TemplateResponse("index.html", {"request": request, "graph_html": graph_html, "info": info})
