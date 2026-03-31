class AppError(Exception):
    def __init__(self, code: str, message: str, details: dict | None = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource}을(를) 찾을 수 없습니다",
            details={"resource": resource, "id": resource_id},
        )


class DuplicateError(AppError):
    """resource는 영문 코드 사용 (예: 'company', 'product')"""

    def __init__(self, resource: str, field: str, existing_id: str | None = None):
        details: dict = {"resource": resource, "field": field}
        if existing_id:
            details["existing_id"] = existing_id
        super().__init__(
            code=f"DUPLICATE_{resource.upper()}",
            message="이미 등록된 항목입니다",
            details=details,
        )


class ValidationError(AppError):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(code="VALIDATION_ERROR", message=message, details=details)
