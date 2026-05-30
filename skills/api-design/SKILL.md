# SKILL: API Design

> REST, GraphQL, tRPC patterns for production APIs.

## Decision Matrix
| Factor | REST | GraphQL | tRPC |
|--------|------|---------|------|
| Best for | Public APIs | Complex queries | TS full-stack |
| Type safety | Manual | Schema | Full end-to-end |
| Caching | HTTP native | Poor | N/A |

## REST Patterns
```
GET    /api/v1/users         # List (paginated)
GET    /api/v1/users/:id     # Get one
POST   /api/v1/users         # Create
PATCH  /api/v1/users/:id     # Update
DELETE /api/v1/users/:id     # Delete
```

## Response Format
```typescript
// Success
{ "data": {...}, "meta": { "page": 1, "perPage": 20, "total": 100 } }

// Error
{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }
```

## Status Codes
```
200 OK | 201 Created | 204 No Content
400 Bad Request | 401 Unauthorized | 403 Forbidden
404 Not Found | 409 Conflict | 422 Unprocessable | 429 Rate Limited
500 Internal Server Error
```

## FastAPI Template
```python
@router.get("/", response_model=PaginatedResponse[ProjectOut])
async def list_projects(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user),
):
    query = Project.query.filter_by(user_id=current_user.id)
    total = await query.count()
    items = await query.offset((page - 1) * per_page).limit(per_page).all()
    return {"data": items, "meta": {"page": page, "per_page": per_page, "total": total}}

@router.post("/", response_model=ProjectOut, status_code=201)
async def create_project(data: ProjectCreate, current_user = Depends(get_current_user)):
    return await Project.create(**data.dict(), user_id=current_user.id)
```

## tRPC (TypeScript Full-Stack)
```ts
const t = initTRPC.create()
const protectedProcedure = t.procedure.use(async ({ ctx, next }) => {
  const session = await auth()
  if (!session) throw new TRPCError({ code: "UNAUTHORIZED" })
  return next({ ctx: { session } })
})

export const projectRouter = router({
  list: protectedProcedure.query(async ({ ctx }) => {
    return await db.project.findMany({ where: { userId: ctx.session.user.id } })
  }),
  create: protectedProcedure
    .input(z.object({ name: z.string() }))
    .mutation(async ({ input, ctx }) => {
      return await db.project.create({ data: { ...input, userId: ctx.session.user.id } })
    }),
})
// Usage: trpc.project.list.useQuery() — fully type-safe!
```

## Rate Limiting
```python
@router.post("/")
@limiter.limit("5/minute")
async def create(data: CreateDTO, request: Request):
    ...
```

## Versioning
```
/api/v1/users  (recommended — URL path)
Accept: application/vnd.myapp.v2+json  (header — for subtle changes)
```
