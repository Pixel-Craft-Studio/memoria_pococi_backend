from fastapi import FastAPI
from routers import configuration_router, team_member_router, social_platform_router

app = FastAPI()

# Incluir routers
app.include_router(social_platform_router.router, prefix="/social-platform", tags=["Social Platform"])
app.include_router(team_member_router.router, prefix="/team-member", tags=["Team Member"])
app.include_router(configuration_router.router, prefix="/configuration", tags=["Configuration"])

@app.get("/")
def read_root():
    return {"message": "Alive!"}