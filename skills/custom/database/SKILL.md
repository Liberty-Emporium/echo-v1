---
name: database
description: Work with databases - SQL queries, schema design, migrations, and debugging. Supports PostgreSQL, MySQL, SQLite.
---

# Database

## Common Queries

### Basic CRUD
```sql
-- Select
SELECT * FROM users WHERE active = true ORDER BY created_at DESC;

-- Insert
INSERT INTO products (name, price, category) VALUES ('Widget', 19.99, 'Tools');

-- Update
UPDATE inventory SET quantity = quantity - 1 WHERE id = 123;

-- Delete
DELETE FROM pending_users WHERE created_at < NOW() - INTERVAL '7 days';
```

### Joins
```sql
-- Inner join
SELECT o.id, u.email, o.total FROM orders o
JOIN users u ON o.user_id = u.id;

-- Left join (with null check)
SELECT p.name, c.category FROM products p
LEFT JOIN categories c ON p.category_id = c.id WHERE c.id IS NULL;
```

### Aggregates
```sql
-- Group by
SELECT category, COUNT(*), AVG(price) FROM products GROUP BY category;

-- Having (filter after group)
SELECT user_id, SUM(total) as revenue FROM orders
GROUP BY user_id HAVING SUM(total) > 1000;
```

## Schema Design

### Create Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Add Column
```sql
ALTER TABLE products ADD COLUMN description TEXT;
ALTER TABLE products ADD CONSTRAINT price_check CHECK (price >= 0);
```

## Debugging

```sql
-- Explain query
EXPLAIN ANALYZE SELECT * FROM products WHERE id = 123;

-- Show table size
SELECT pg_size_pretty(pg_total_relation_size('products'));

-- Find slow queries (PostgreSQL)
SELECT query, calls, mean_time FROM pg_stat_statements
ORDER BY mean_time DESC LIMIT 10;
```