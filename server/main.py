from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.exception_handlers import catch_middleware_exceptions
from routes.upload_files import router as upload_router
from routes.chat import router as query_router


app = FastAPI(title="Bussiness Assistant", description="API for Bussiness assistance chatbot")
#
##COrs Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

##Middleware exception handlers
app.middleware("http")(catch_middleware_exceptions)


##Routers
# 1. Upload pdf documents
app.include_router(upload_router)

# 2. chat
app.include_router(query_router)



