# Worker Redis Image Processing System

Sistema distribuido para procesamiento de imágenes utilizando Redis, FastAPI y múltiples workers paralelos con Docker Compose.

---

# 🚀 Características

* Arquitectura distribuida basada en workers
* Cola de trabajos con Redis
* Backend REST API con FastAPI
* Procesamiento paralelo de imágenes
* Docker Compose listo para despliegue
* Escalable horizontalmente
* Manejo de estados de jobs
* Sistema desacoplado y modular

---

# 🧱 Arquitectura

```text
Frontend / Cliente
        │
        ▼
 FastAPI Backend
        │
        ▼
     Redis Queue
        │
 ┌───────────────┐
 │    Workers    │
 │   worker1     │
 │   worker2     │
 │   worker3     │
 └───────────────┘
        │
        ▼
 Procesamiento de imágenes
```

---

# 📂 Estructura del Proyecto

```text
.
├── backend/
│   ├── main.py
│   ├── jobs.py
│   ├── tasks.py
│   ├── worker.py
│   └── requirements.txt
│
├── frontend/
├── uploads/
├── processed/
├── images/
├── docker-compose.yml
├── redis_client.py
└── README.md
```

---

# ⚙️ Tecnologías Utilizadas

* Python 3.12+
* FastAPI
* Redis
* Docker
* Docker Compose

---

# 🐳 Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/JavierNLopez/worker-redis-image.git
cd worker-redis-image
```

---

## 2. Levantar servicios

```bash
docker compose up --build -d
```

---

# 🌐 Servicios

| Servicio        | Puerto |
| --------------- | ------ |
| FastAPI Backend | 8000   |
| Redis           | 6379   |

---

# 📌 API Endpoints

## Crear Job

```http
POST /jobs
```

Respuesta:

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

---

## Obtener Estado del Job

```http
GET /jobs/{job_id}
```

Respuesta:

```json
{
  "status": "done",
  "result": "ok"
}
```

---

## Health Check

```http
GET /
```

Respuesta:

```json
{
  "status": "ok",
  "service": "backend"
}
```

---

# 🔥 Estados de Jobs

| Estado     | Descripción                 |
| ---------- | --------------------------- |
| queued     | Trabajo en cola             |
| processing | Procesando                  |
| done       | Completado                  |
| error      | Error durante procesamiento |

---

# 🧠 Redis Job Structure

Cada trabajo se almacena utilizando:

```text
job:<job_id>
```

como HASH en Redis.

Ejemplo:

```text
job:1234-abcd
```

Campos:

* status
* result
* worker

---

# 🚀 Escalabilidad

Puedes aumentar fácilmente el número de workers:

```bash
docker compose up --scale worker=5
```

---

# 📦 Docker

Levantar contenedores:

```bash
docker compose up --build
```

Detener servicios:

```bash
docker compose down
```

---

# 🛠 Desarrollo

Ver logs:

```bash
docker logs -f backend
docker logs -f worker1
```

Entrar a Redis CLI:

```bash
docker exec -it redis redis-cli
```

---

# 📌 Futuras Mejoras

* Dashboard en tiempo real
* WebSockets / SSE
* Auto-scaling de workers
* Retry automático de jobs
* Persistencia avanzada
* Balanceo de carga

---

# 👨‍💻 Autor

Desarrollado por Javier Lopez.

GitHub:
https://github.com/JavierNLopez
