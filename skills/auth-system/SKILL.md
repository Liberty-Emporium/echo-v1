# SKILL: Authentication System

> OAuth, JWT, magic links, RBAC, session management.

## Methods Compared
| Method | Best For | Complexity |
|--------|----------|------------|
| NextAuth.js | Next.js, OAuth | Low |
| Clerk | Managed auth | Very Low |
| JWT + bcrypt | APIs, SPAs | Medium |
| Magic Links | No-password | Medium |

## NextAuth v5
```ts
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import { PrismaAdapter } from "@auth/prisma-adapter"

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [Google],
  session: { strategy: "jwt" },
  callbacks: {
    async session({ session, token }) {
      session.user.id = token.sub!
      return session
    },
  },
})
```

## JWT (APIs)
```python
from jose import jwt
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"])

# Hash password
hash = pwd.hash(password)

# Create token
token = jwt.encode({"sub": user.id, "exp": ...}, SECRET_KEY, "HS256")

# Verify
payload = jwt.decode(token, SECRET_KEY, ["HS256"])

# Dependency
async def get_current_user(token = Depends(HTTPBearer())):
    payload = jwt.decode(token.credentials, SECRET_KEY, ["HS256"])
    return await get_user(payload["sub"])

# Role check
def require_role(*roles):
    async def checker(user = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, "Forbidden")
        return user
    return checker
```

## RBAC
```sql
CREATE TYPE user_role AS ENUM ('user', 'moderator', 'admin', 'superadmin');

-- Permission table
CREATE TABLE permissions (
    role user_role NOT NULL,
    resource TEXT NOT NULL,
    action TEXT NOT NULL,
    PRIMARY KEY (role, resource, action)
);
```

## Security Checklist
- [ ] bcrypt (cost 12+)
- [ ] JWT expiry (15 min access, 7 day refresh)
- [ ] HTTPS + HSTS
- [ ] Rate limit auth endpoints (5/min)
- [ ] Same error for wrong email vs wrong password
- [ ] Account lockout after 5 failures
- [ ] Audit log all auth events
- [ ] CSRF protection
- [ ] CORS restricted
