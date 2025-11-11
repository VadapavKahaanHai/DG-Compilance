from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class DGComplianceException(Exception):
    """Base exception for DG compliance errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class DataNotFoundException(DGComplianceException):
    """Raised when data is not found"""
    def __init__(self, message: str = "Data not found"):
        super().__init__(message, status_code=404)


class InvalidCargoException(DGComplianceException):
    """Raised when cargo data is invalid"""
    def __init__(self, message: str = "Invalid cargo data"):
        super().__init__(message, status_code=422)


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(DGComplianceException)
    async def dg_compliance_exception_handler(request: Request, exc: DGComplianceException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error", "detail": str(exc)}
        )