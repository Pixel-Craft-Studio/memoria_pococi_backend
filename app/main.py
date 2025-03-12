from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    configuration_router,
    team_member_router,
    social_platform_router,
    profile_router,
    login_router,
    image_router,
    timeline_category_router,
    contact_us_router,
    timeline_year_router,
    timeline_history_router,
)

app = FastAPI()


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    """
    Cambia la clave 'detail' por 'message' en errores HTTPException
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login_router.router, prefix="/login", tags=["Login"])
app.include_router(profile_router.router, prefix="/profiles", tags=["Profile"])
app.include_router(
    configuration_router.router, prefix="/configuration", tags=["Configuration"]
)
app.include_router(
    social_platform_router.router, prefix="/social-platform", tags=["Social Platform"]
)
app.include_router(
    team_member_router.router, prefix="/team-member", tags=["Team Member"]
)

app.include_router(
    timeline_category_router.router, prefix="/timeline-category", tags=["Categories"]
)

app.include_router(
    timeline_year_router.router, prefix="/timeline-year", tags=["Timeline Year"]
)

app.include_router(
    timeline_history_router.router,
    prefix="/timeline-history",
    tags=["Timeline History"],
)

app.include_router(contact_us_router.router, prefix="/contact-us", tags=["Contact-us"])

app.include_router(image_router.router, prefix="/image", tags=["Images"])


@app.get("/")
def read_root():
    return {"message": "Alive!"}
