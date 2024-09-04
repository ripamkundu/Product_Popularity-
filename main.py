from fastapi import FastAPI
from routers.items import router as product_router
import uvicorn

app = FastAPI(
    title="Product Catalog API",
    description="API for managing a product catalog with CRUD operations, search, and popularity calculation",
    version="1.0.0",
    docs_url="/dx",
)

# Include the products router
app.include_router(product_router)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Catalog API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
