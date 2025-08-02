from fastapi import APIRouter
from app.db.models.controllers.authentification_controllers import router as auth_router
from app.db.models.controllers.todolist_controllers import router as todolist_router

router=APIRouter(prefix="/app")
router.include_router(auth_router, prefix="/auth", tags=["authentification"])
router.include_router(todolist_router, prefix="/todolists", tags=["todolists"])
