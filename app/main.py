from fastapi import FastAPI

from app.api.router import router


def get_application(*, debug: bool = False) -> FastAPI:
    application = FastAPI(
        title="Python",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url=None,
        description="Python",
        debug=debug,
    )
    application.include_router(router=router, prefix="/api/v1")

    return application


app = get_application()
