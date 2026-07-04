# 🚀 GUÍA DE IMPLEMENTACIÓN: SOLUCIONES CON IA DEEPSEEK

## Estado: ✅ LISTO PARA USAR

He generado una **aplicación completa con IA integrada** usando Deepseek. Aquí te muestro cómo activarla.

---

## 📋 PASO 1: Configurar Variables de Entorno

### 1.1 Crea archivo `.env` en la carpeta `backend/`

```bash
cd backend
notepad .env
```

### 1.2 Copia y pega esto en `.env`:

```
DEEPSEEK_API_KEY=sk_tu_api_key_aqui
DEEPSEEK_MODEL=deepseek-chat
DATABASE_URL=sqlite:///./scanner.db
SECRET_KEY=tu_secret_key_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
LOG_LEVEL=INFO
```

**⚠️ IMPORTANTE:** 
- Reemplaza `sk_tu_api_key_aqui` con tu **verdadera API key de Deepseek**
- NO compartas este archivo ni su contenido

---

## 📦 PASO 2: Instalar Dependencias

```bash
cd backend

# Instalar librerías necesarias para IA
pip install requests python-dotenv
```

---

## 🔧 PASO 3: Modificar `backend/main.py`

Agregar estas líneas al inicio del archivo (después de los imports existentes):

```python
# Agregar estas líneas después de los imports
from solutions_routes import router as solutions_router
from ai_service import ai_service
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... resto del código existente ...

# Agregar esta línea DESPUÉS de crear la app (after app = FastAPI(...))
# Incluir el router de soluciones con IA
app.include_router(solutions_router)

logger.info("✅ Soluciones con IA Deepseek inicializadas")
```

---

## 🎨 PASO 4: Instalar Dependencias del Frontend

```bash
cd frontend

# Instalar syntax highlighter para mostrar código
npm install react-syntax-highlighter
npm install --save-dev @types/react-syntax-highlighter
```

---

## 🖼️ PASO 5: Integrar Componente en UI

### Opción A: Agregar Tab nuevo en `frontend/src/app/page.tsx`

```typescript
// Agregar al inicio del archivo, en imports:
import { AISolutionGenerator } from "@/components/AISolutionGenerator";

// Agregar a la lista de tabs (busca donde dice ["Scanner", "Resultados", ...])
const tabs = ["Scanner", "Resultados", "Historial", "Reporte", "🤖 Soluciones IA"];

// Agregar tab nuevo antes del último cierre de main (antes de </main>)
{activeTab === "🤖 Soluciones IA" && (
  <div className="animate-in fade-in duration-300">
    <h1 className="text-2xl font-bold text-white mb-6">Generador de Soluciones con IA</h1>
    <AISolutionGenerator 
      vulnerabilityType="XSS" 
      targetStack="node" 
    />
  </div>
)}
```

### Opción B: Página dedicada (mejor)

Crear `frontend/src/app/solutions/page.tsx`:

```typescript
"use client";

import { AISolutionGenerator } from "@/components/AISolutionGenerator";
import { useState } from "react";

export default function SolutionsPage() {
  const [selectedVuln, setSelectedVuln] = useState("XSS");
  
  const commonVulnerabilities = [
    "XSS",
    "SQLi",
    "CSRF",
    "Open Redirect",
    "SSRF",
    "Path Traversal",
    "Authentication Bypass",
    "Info Disclosure"
  ];

  return (
    <div className="min-h-screen bg-[#0f1115] text-gray-300 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">🤖 Soluciones con IA</h1>
        <p className="text-gray-400 mb-8">
          Genera soluciones automáticas para vulnerabilidades usando Deepseek IA
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar con vulnerabilidades */}
          <div className="lg:col-span-1">
            <div className="bg-[#161920] border border-gray-800 rounded-lg p-4 sticky top-6">
              <h3 className="text-sm font-semibold text-white mb-3">Vulnerabilidades Comunes</h3>
              <div className="space-y-2">
                {commonVulnerabilities.map(vuln => (
                  <button
                    key={vuln}
                    onClick={() => setSelectedVuln(vuln)}
                    className={`w-full text-left px-3 py-2 rounded transition-colors ${
                      selectedVuln === vuln
                        ? "bg-blue-600 text-white"
                        : "text-gray-300 hover:bg-[#1a1d24]"
                    }`}
                  >
                    {vuln}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main content */}
          <div className="lg:col-span-3">
            <AISolutionGenerator 
              vulnerabilityType={selectedVuln}
              targetStack="node"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## ✅ PASO 6: Verificar Funcionamiento

### Backend:
```bash
cd backend
python -m uvicorn main:app --reload
```

Deberías ver: `✅ Soluciones con IA Deepseek inicializadas`

### Frontend:
```bash
cd frontend
npm run dev
```

Accede a: `http://localhost:3000`

---

## 🧪 PRUEBA LA API DIRECTAMENTE

Abre una terminal y ejecuta:

```bash
curl -X POST "http://127.0.0.1:8000/api/solutions/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "vulnerability_type": "XSS",
    "target_stack": "node",
    "use_cache": true
  }'
```

Deberías recibir una respuesta JSON completa con la solución.

---

## 📊 ENDPOINTS DISPONIBLES

| Endpoint | Método | Descripción |
|----------|--------|------------|
| `/api/solutions/generate` | POST | Generar solución única |
| `/api/solutions/generate-multiple` | POST | Generar múltiples soluciones |
| `/api/solutions/available-stacks` | GET | Ver stacks soportados |
| `/api/solutions/cache-status` | GET | Ver estado del caché |
| `/api/solutions/cache-clear` | POST | Limpiar caché |

---

## 🎯 FLUJO DE FUNCIONAMIENTO

```
Usuario selecciona vulnerabilidad
        ↓
Frontend envía a API
        ↓
Backend consulta Deepseek IA
        ↓
IA genera solución (código + pasos)
        ↓
Respuesta se cachea (evita repetir requests)
        ↓
Frontend muestra con Syntax Highlighting
```

---

## 📁 ARCHIVOS CREADOS/MODIFICADOS

### Nuevos:
- ✅ `backend/ai_service.py` - Servicio de IA
- ✅ `backend/solutions_routes.py` - Rutas API
- ✅ `backend/.env.example` - Ejemplo de configuración
- ✅ `frontend/src/components/AISolutionGenerator.tsx` - Componente UI

### Por modificar:
- 📝 `backend/main.py` - Agregar imports y router
- 📝 `frontend/src/app/page.tsx` - Opcional: Agregar tab

---

## 💡 CARACTERÍSTICAS

✅ **Generación en tiempo real** - IA responde en 3-5 segundos  
✅ **Cacheo inteligente** - No gasta tokens en consultas repetidas  
✅ **Múltiples stacks** - Node, Python, PHP, Java, .NET, etc  
✅ **Código formateado** - Syntax highlighting automático  
✅ **Pasos detallados** - Soluciones con pasos específicos  
✅ **Referencias** - Links a OWASP, CWE, etc  
✅ **Bajo costo** - Deepseek es 10x más barato que OpenAI  

---

## 🔒 SEGURIDAD

- ✅ API key guardada en `.env` (nunca en código)
- ✅ Variables de entorno cargadas con `python-dotenv`
- ✅ Logging de errores sin exponer credenciales
- ✅ Timeouts configurados (30 segundos)
- ✅ Error handling robusto

---

## 🚨 TROUBLESHOOTING

### Error: "DEEPSEEK_API_KEY no configurada"
**Solución:** Verifica que `.env` exista en `backend/` y tenga la key correcta

### Error: 401 Unauthorized
**Solución:** Reemplaza `sk_tu_api_key_aqui` con tu **verdadera API key**

### Componente no aparece
**Solución:** Verifica que `AISolutionGenerator.tsx` esté en `frontend/src/components/`

### API lenta
**Solución:** Deepseek puede tardar 3-5 segundos, es normal. Aumenta timeout si necesario.

---

## 🎬 PRÓXIMOS PASOS

1. ✅ Configura `.env` con tu API key
2. ✅ Instala dependencias
3. ✅ Modifica `main.py`
4. ✅ Prueba la API con curl
5. ✅ Agrega componente al frontend
6. ✅ ¡Usa la IA!

---

## 📞 SOPORTE

Si tienes problemas:
1. Verifica que Deepseek API está activa
2. Comprueba que la API key es correcta
3. Asegúrate que internet funciona
4. Revisa los logs en consola

**Estado:** 🟢 **LISTO PARA USAR**

Todos los archivos están creados y listos. Solo necesitas:
1. Configurar `.env`
2. Instalar dependencias  
3. Modificar `main.py`
4. ¡Disfrutar!
