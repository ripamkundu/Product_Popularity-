from datetime import datetime
from fastapi import APIRouter, HTTPException
from database.items import (
    create_product,
    get_product_by_id,
    get_all_product_item,
    update_product,
    delete_product,
    search_product_item,
    get_product_popularity,
)
from models.items import ProductCreate, ProductUpdate

router = APIRouter()


# Create Product Router
@router.post("/product_create", response_model=ProductCreate)
def create(product: ProductCreate):
    try:
        product_id = create_product(
            product.name,
            product.description,
            product.price,
            product.inventory_count,
            product.category,
        )
        return ProductCreate(
            id=product_id,
            name=product.name,
            description=product.description,
            price=product.price,
            inventory_count=product.inventory_count,
            category=product.category,
            sales_count=0,
            created_at=datetime.now(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Product creation failed: {str(e)}"
        )


# Get Product by ID
@router.get("/all_product/{product_id}", response_model=dict)
def get_product(product_id: int):
    try:
        product = get_product_by_id(product_id)
        return {
            "id": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "inventory_count": product[4],
            "category": product[5],
            "sales_count": product[6],
            "created_at": product[7],
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


# Get All Products
@router.get("/product_list", response_model=list)
def get_products():
    try:
        products = get_all_product_item()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update Product
@router.put("/update/{product_id}", response_model=dict)
def update(product_id: int, product: ProductUpdate):
    try:
        updated = update_product(
            product_id,
            product.name,
            product.description,
            product.price,
            product.inventory_count,
            product.category,
        )
        if updated:
            return {"message": "Product updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete Product
@router.delete("/delete/{product_id}", response_model=dict)
def delete(product_id: int):
    try:
        deleted = delete_product(product_id)
        if deleted:
            return {"message": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Search Products
@router.get("/search/{query_string}", response_model=list)
def search(query_string: str):
    try:
        results = search_product_item(query_string)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get Product Popularity
@router.get("/popularity/{product_id}", response_model=dict)
def get_popularity(product_id: int):
    try:
        popularity_score = get_product_popularity(product_id)
        if popularity_score is not None:
            return {"product_id": product_id, "popularity_score": popularity_score}
        else:
            raise HTTPException(
                status_code=404, detail="Product not found or has no sales data"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
