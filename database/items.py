from database.con import connect
from fastapi import HTTPException


# Create Product
def create_product(name, description, price, inventory_count, category):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """INSERT INTO product_item (name, description, price, inventory_count, category)
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (name, description, price, inventory_count, category)
        cursor.execute(query, values)
        conn.commit()
        product_id = cursor.lastrowid
        return product_id
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Product creation failed: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()


# Read (Get) Product by ID
def get_product_by_id(product_id):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "SELECT * FROM product_item WHERE id = %s"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Read (Get) All Products
def get_all_product_item():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "SELECT * FROM product_item"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching products: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()


# Update Product
def update_product(product_id, name, description, price, inventory_count, category):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """UPDATE product_item 
                   SET name = %s, description = %s, price = %s, inventory_count = %s, category = %s
                   WHERE id = %s"""
        values = (name, description, price, inventory_count, category, product_id)
        cursor.execute(query, values)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product update failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()


# Delete Product
def delete_product(product_id):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "DELETE FROM product_item WHERE id = %s"
        cursor.execute(query, (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return True
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Product deletion failed: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()


# Search Products by Name, Description, or Category
def search_product_item(query_string):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """SELECT * FROM product_item WHERE 
                   name LIKE %s OR 
                   description LIKE %s OR 
                   category LIKE %s"""
        search_term = f"%{query_string}%"
        cursor.execute(query, (search_term, search_term, search_term))
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product search failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()


# Calculate Product Popularity Score
def get_product_popularity(product_id):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "SELECT sales_count FROM product_item WHERE id = %s"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()

        if result and result[0] is not None:
            try:
                sales_count = int(result[0])
                popularity_score = sales_count / 100
                return popularity_score
            except ValueError:
                raise HTTPException(status_code=500, detail="Invalid sales_count value")
        else:
            return None
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Popularity calculation failed: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()
