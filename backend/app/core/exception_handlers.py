from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError, BusinessRuleError, DuplicateError, NotFoundError, ValidationError


def register_exception_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": exc.code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(DuplicateError)
    async def duplicate_handler(request: Request, exc: DuplicateError):
        return JSONResponse(
            status_code=409,
            content={"error": exc.code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content={"error": exc.code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(BusinessRuleError)
    async def business_rule_handler(request: Request, exc: BusinessRuleError):
        return JSONResponse(
            status_code=409,
            content={"error": exc.code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=500,
            content={"error": exc.code, "message": exc.message, "details": exc.details},
        )
