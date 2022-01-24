import logging

from fastapi import FastAPI, Request, Body, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from utils.format_error import format_error

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/get-frameworks-list/")
async def get_frameworks_list():
    try:
        return ["Svelte", "Vue", "React", "Other"]
    except:
        logging.error(format_error("main.py"))


@app.post("/api/submit-framework/")
async def submit_framework(selected_framework: str = Body(..., embed=True)):
    try:
        return { "message": "You chose " + selected_framework }
    except:
        logging.error(format_error("main.py"))


########################################
########## Static File Routes ##########
########################################
"""
In a traditional production deployment (where frontend templates are rendered by the server) requests for static assets (HTML, CSS, JavaScript, or image files) will be routed to this endpoint and return the necessary files. However, if you are using Docker containers inside of a Kubernetes cluster for production, then requests for static assets are handled and routed by a web server (e.g. Nginx, Express.js). If you are using Docker and Kubernetes, then the following path will not be used.

During development, however, Svelte uses a development server that will manage the static assets (including the index.html or app.html files). So no requests for static assets will be sent to the backend during development.
"""
@app.get("/_app/{rest_of_path:path}")
def assets(rest_of_path: str):
    try:
        return FileResponse("../client/build/_app/" + rest_of_path)
    except:
        logging.error(format_error("main.py"))


"""
Routes for a specific file, like the favicon.png file, work like this.
"""
@app.get("/favicon.png")
def favicon(rest_of_path: str):
    try:
        return FileResponse("../build/client/build/favicon.png")
    except:
        logging.error(format_error("main.py"))
        

"""
This is the catch-all route for a traditional production deployment and should be the last route defined (see https://stackoverflow.com/questions/63069190/how-to-capture-arbitrary-paths-at-one-route-in-fastapi). For a traditional production app, if any requests do not have a matching route, then this catch-all route would be configured to return a 404 error page (e.g. 404.html), but SPAs work differently. When creating an SPA, this route should return the index.html file. Also, with an SPA any 404 errors should be handle by the frontend framework rather than a server-side catch-all route like the following route. SvelteKit uses an __error.svelte page to handle 404 errors (see https://kit.svelte.dev/docs#layouts-error-pages). (NOTE: SvelteKit uses app.html by default, but that file has been changed to index.html because that is typically what web servers like Nginx expect.)

For a Docker and Kubernetes production deployment, you would have to configure how 404 errors are handled in Nginx or Kubernetes or maybe both.
"""
@app.get("/{full_path:path}")
def catch_all(full_path: str):
    try:
        # If you are using a multi-container Docker environment in production, then uncomment the following line before you deploy to production.
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

        # Uncomment the following line if you want to use a local, non-Docker environment during development:
        # return FileResponse("../client/build/src/index.html", media_type="text/html")

        # NOTE: You do not need to do any other configurations to this route if you are developing inside of a multi-container Docker environment. See the notes above the `@app.get("/_app/{rest_of_path:path}")` route.
    except:
        logging.error(format_error("main.py"))
