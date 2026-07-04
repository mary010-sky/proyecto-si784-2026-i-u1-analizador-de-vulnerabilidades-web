# 🚀 PLAN DE IMPLEMENTACIÓN: LOGIN + API DE REGISTROS

**Objetivo:** Agregar autenticación segura y sistema de conteo de usuarios registrados

---

## FASE 1: INFRAESTRUCTURA DE SEGURIDAD (2-3 horas)

### 1.1 Instalar Dependencias

```bash
cd backend
pip install bcrypt python-jose python-multipart python-dotenv slowapi
pip install pydantic-settings
```

### 1.2 Crear Variables de Entorno

**Archivo: `backend/.env`**

```env
# Generare una clave con: openssl rand -hex 32
SECRET_KEY=tu_clave_secreta_super_segura_de_64_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./scanner.db
DEBUG=False
```

### 1.3 Actualizar Modelo de Base de Datos

**Archivo: `backend/models.py` (COMPLETO)**

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # ← NUEVO: Asociar con usuario
    target_url = Column(String, index=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    result_summary = Column(Text, nullable=True)
```

---

## FASE 2: AUTENTICACIÓN JWT (2-3 horas)

### 2.1 Crear Módulo de Seguridad

**Archivo: `backend/security.py` (NUEVO)**

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "tu-secret-key-cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hashear contraseña con bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña contra hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token JWT de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verificar y decodificar JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """Dependencia para proteger endpoints"""
    token = credentials.credentials
    user_data = verify_token(token)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data
```

### 2.2 Crear Esquemas Pydantic

**Archivo: `backend/schemas.py` (NUEVO)**

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# ==================== USER ====================
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# ==================== TOKENS ====================
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: int
    email: str

# ==================== SCAN ====================
class ScanRequest(BaseModel):
    url: str
    modules: list[str]
    depth: int = 2
    timeout: int = 10

class ScanResponse(BaseModel):
    id: int
    target_url: str
    status: str
    result_summary: dict
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== STATISTICS ====================
class UserStatsResponse(BaseModel):
    total_users: int
    users_today: int
    users_this_week: int
    users_this_month: int
    growth_rate: float

class UserByDateResponse(BaseModel):
    date: str
    count: int
```

---

## FASE 3: ENDPOINTS DE AUTENTICACIÓN (2-3 horas)

### 3.1 Crear Rutas de Autenticación

**Archivo: `backend/auth_routes.py` (NUEVO)**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
import models
import schemas
from security import (
    hash_password, verify_password, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""

    # Validar que no exista email
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Validar que no exista username
    db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    # Validar contraseña fuerte
    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="Contraseña muy corta")
    if not any(c.isupper() for c in user_data.password):
        raise HTTPException(status_code=400, detail="Contraseña debe incluir mayúscula")
    if not any(c.isdigit() for c in user_data.password):
        raise HTTPException(status_code=400, detail="Contraseña debe incluir número")

    # Crear usuario
    db_user = models.User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=schemas.Token)
async def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login de usuario"""

    # Buscar usuario
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if not db_user or not verify_password(user_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    # Crear token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.id, "email": db_user.email},
        expires_delta=access_token_expires
    )

    # Actualizar último login
    db_user.last_login = datetime.utcnow()
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Obtener información del usuario actual"""
    user = db.query(models.User).filter(models.User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout (simplemente valida que el token es válido)"""
    return {"message": "Logout exitoso"}
```

---

## FASE 4: API DE ESTADÍSTICAS (1-2 horas)

### 4.1 Crear Rutas de Estadísticas

**Archivo: `backend/stats_routes.py` (NUEVO)**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from database import get_db
import models
import schemas
from security import get_current_user

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("/users/count", response_model=dict)
async def get_user_count(db: Session = Depends(get_db)):
    """Total de usuarios registrados"""
    count = db.query(func.count(models.User.id)).scalar()
    return {"total_users": count or 0}

@router.get("/users/today", response_model=dict)
async def get_users_today(db: Session = Depends(get_db)):
    """Usuarios registrados hoy"""
    today = datetime.utcnow().date()
    count = db.query(func.count(models.User.id)).filter(
        func.date(models.User.created_at) == today
    ).scalar()
    return {"users_today": count or 0}

@router.get("/users/this-week", response_model=dict)
async def get_users_this_week(db: Session = Depends(get_db)):
    """Usuarios registrados esta semana"""
    week_ago = datetime.utcnow() - timedelta(days=7)
    count = db.query(func.count(models.User.id)).filter(
        models.User.created_at >= week_ago
    ).scalar()
    return {"users_this_week": count or 0}

@router.get("/users/this-month", response_model=dict)
async def get_users_this_month(db: Session = Depends(get_db)):
    """Usuarios registrados este mes"""
    month_ago = datetime.utcnow() - timedelta(days=30)
    count = db.query(func.count(models.User.id)).filter(
        models.User.created_at >= month_ago
    ).scalar()
    return {"users_this_month": count or 0}

@router.get("/users/timeline", response_model=list[schemas.UserByDateResponse])
async def get_users_timeline(days: int = 30, db: Session = Depends(get_db)):
    """Registros de usuarios por día (últimos N días)"""
    start_date = datetime.utcnow() - timedelta(days=days)

    results = db.query(
        func.date(models.User.created_at).label("date"),
        func.count(models.User.id).label("count")
    ).filter(
        models.User.created_at >= start_date
    ).group_by(
        func.date(models.User.created_at)
    ).order_by(
        func.date(models.User.created_at)
    ).all()

    return [
        {"date": str(date), "count": count}
        for date, count in results
    ]

@router.get("/users/growth-rate", response_model=dict)
async def get_growth_rate(db: Session = Depends(get_db)):
    """Tasa de crecimiento de usuarios"""
    today_count = db.query(func.count(models.User.id)).filter(
        func.date(models.User.created_at) == datetime.utcnow().date()
    ).scalar() or 0

    yesterday_count = db.query(func.count(models.User.id)).filter(
        func.date(models.User.created_at) == (datetime.utcnow() - timedelta(days=1)).date()
    ).scalar() or 0

    growth_rate = ((today_count - yesterday_count) / max(yesterday_count, 1)) * 100

    return {
        "today": today_count,
        "yesterday": yesterday_count,
        "growth_rate_percentage": round(growth_rate, 2)
    }
```

---

## FASE 5: ACTUALIZAR MAIN.PY

### 5.1 Estructura Completa de main.py

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from auth_routes import router as auth_router
from stats_routes import router as stats_router
from security import get_current_user
import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Web Vulnerability Scanner API")

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# ==================== MIDDLEWARES ====================

# CORS restringido (NO abierto)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

# Security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# ==================== RUTAS ====================

# Incluir routers
app.include_router(auth_router)
app.include_router(stats_router)

# Health check (sin autenticación)
@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request):
    return {"status": "healthy"}

# Endpoint de escaneo (PROTEGIDO)
@app.post("/api/scan", response_model=schemas.ScanResponse)
@limiter.limit("5/minute")  # Rate limit
async def scan(
    request_data: schemas.ScanRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Realizar escaneo (requiere autenticación)"""

    # Validar URL
    if not request_data.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL inválida")

    # Crear escaneo
    scan = models.Scan(
        user_id=current_user["user_id"],
        target_url=request_data.url,
        status="running"
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # TODO: Realizar escaneo real aquí

    return scan

@app.get("/api/scans")
async def get_user_scans(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener escaneos del usuario actual"""
    scans = db.query(models.Scan).filter(
        models.Scan.user_id == current_user["user_id"]
    ).order_by(models.Scan.created_at.desc()).all()
    return scans

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## FASE 6: ACTUALIZAR FRONTEND

### 6.1 Crear contexto de autenticación

**Archivo: `frontend/src/context/AuthContext.tsx` (NUEVO)**

```typescript
'use client';

import { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: number;
  email: string;
  username: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Restaurar token del localStorage
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
      setToken(savedToken);
      // TODO: Validar token
    }
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) throw new Error('Login falló');

      const data = await response.json();
      setToken(data.access_token);
      setUser(data.user);
      localStorage.setItem('token', data.access_token);
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, username: string, password: string, fullName?: string) => {
    setLoading(true);
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password, full_name: fullName }),
      });

      if (!response.ok) throw new Error('Registro falló');

      const data = await response.json();
      setUser(data);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
}
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

```
FASE 1: Infraestructura
  [ ] Instalar dependencias
  [ ] Crear .env
  [ ] Actualizar models.py
  [ ] Crear security.py
  [ ] Crear schemas.py

FASE 2: Autenticación
  [ ] Crear auth_routes.py
  [ ] Registrar router en main.py
  [ ] Probar con Postman
  [ ] Crear tests

FASE 3: Estadísticas
  [ ] Crear stats_routes.py
  [ ] Registrar router en main.py
  [ ] Probar endpoints
  [ ] Optimizar queries

FASE 4: Frontend
  [ ] Crear AuthContext
  [ ] Crear páginas Login/Register
  [ ] Integrar Context Provider
  [ ] Crear Dashboard de estadísticas

FASE 5: Testing & Seguridad
  [ ] Tests unitarios
  [ ] Tests de integración
  [ ] Verificar HTTPS
  [ ] Penetration testing básico

FASE 6: Despliegue
  [ ] Configurar variables en producción
  [ ] Realizar backup de BD
  [ ] Desplegar backend
  [ ] Desplegar frontend
  [ ] Monitoreo activo
```

---

## 🔒 SEGURIDAD: PUNTOS CLAVE

1. ✅ **Contraseñas:** Siempre hashear con bcrypt
2. ✅ **Tokens:** Expiración corta + refresh tokens
3. ✅ **CORS:** Solo dominios permitidos
4. ✅ **Rate Limiting:** 5 intentos login/hora
5. ✅ **HTTPS:** En producción OBLIGATORIO
6. ✅ **Variables de Entorno:** NUNCA en código
7. ✅ **Validación:** Todos los inputs
8. ✅ **Logging:** Auditoría de acciones

---

## 📞 SIGUIENTES PASOS

1. ¿Quieres que implemente todo el código automáticamente?
2. ¿Necesitas ejemplos de pruebas con Postman?
3. ¿Quieres agregar 2FA (autenticación de dos factores)?
4. ¿Quieres OAuth2 (login con Google/GitHub)?

**Responde sí/no para proceder con la implementación.**
