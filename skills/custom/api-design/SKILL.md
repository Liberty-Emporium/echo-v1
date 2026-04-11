---
name: api-design
description: Design and build REST APIs. Use when you need to create API endpoints, design routes, handle JSON requests/responses, or implement authentication.
---

# API Design

## RESTful Routes

### Standard CRUD
| Method | Route | Description |
|--------|-------|-------------|
| GET | /products | List all |
| GET | /products/:id | Get one |
| POST | /products | Create |
| PUT | /products/:id | Update |
| DELETE | /products/:id | Delete |

### Nested Resources
```
/users/:user_id/orders
/users/:user_id/orders/:order_id
```

## Flask API

```python
from flask import jsonify, request

@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    products = get_all_products(category=category)
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product.create(**data)
    return jsonify(product.to_dict()), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.update(product_id, **data)
    return jsonify(product.to_dict())
```

## Response Format

```json
// Success
{
  "success": true,
  "data": { ... },
  "message": "Created"
}

// Error
{
  "success": false,
  "error": "Not found",
  "code": 404
}

// Pagination
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

## Authentication

### Bearer Token (JWT)
```python
from flask import request

@app.route('/api/protected')
def protected():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    payload = jwt_decode(token)
    # validate and proceed
```

## Best Practices

- Use plural nouns: `/products` not `/product`
- Version APIs: `/api/v1/`
- Return proper status codes
- Paginate list endpoints
- Use ISO 8601 dates