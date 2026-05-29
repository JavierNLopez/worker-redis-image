# 🎬 Distributed Image Processing System ☁️

## 📚 Información del Proyecto
🎓 **Materia:** Programación web - TECNM Campus ITT  
👨‍💻 **Autor:** Javier N. López Prudencio  
📅 **Fecha:** 2026/05/29  

## 🎯 Descripción
Sistema web moderno y escalable para la subida y procesamiento distribuido de imágenes utilizando arquitectura basada en Redis, workers y Docker.

Este proyecto permite:

- ✔ Subir imágenes desde una interfaz web
- ✔ Procesar imágenes de forma asíncrona
- ✔ Gestionar múltiples workers simultáneamente
- ✔ Consultar estados en tiempo real
- ✔ Escalar horizontalmente con Docker Compose

---

## 🚀 Características

- 🖼️ Subida de imágenes
- ⚡ Procesamiento distribuido
- 🔄 Cola de tareas con Redis
- 📡 API REST con FastAPI
- 🐳 Contenedores Docker
- 🌐 Frontend con Nginx
- 📊 Monitoreo de tareas
- 📈 Escalabilidad horizontal

---

## ⚙️ Tecnologías

| Tecnología | Uso |
|---|---|
| 🐍 Python | Backend y workers |
| ⚡ FastAPI | API REST |
| 🔴 Redis | Cola de tareas |
| 🐳 Docker | Contenedores |
| 🧩 Docker Compose | Orquestación |
| 🌐 Nginx | Frontend |
| 🎨 HTML/CSS/JS | Interfaz web |

---

## 🏗️ Arquitectura

```text
Frontend (Nginx)
       │
       ▼
FastAPI Backend
       │
       ▼
Redis Queue
       │
 ┌───────────────┐
 │   Workers     │
 │ Worker 1      │
 │ Worker 2      │
 │ Worker 3      │
 │ Worker N      │
 └───────────────┘
       │
       ▼
Procesamiento de Imágenes
```

---

## 📂 Estructura del Proyecto

```text
worker-redis-image/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── worker/
│   ├── worker.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── docker-compose.yml
└── README.md
```

---

## ▶️ Ejecución del Proyecto

### 🔨 Construir contenedores

```bash
docker compose build
```

### 🚀 Levantar servicios

```bash
docker compose up -d --scale worker=5
```

### 📦 Ver contenedores activos

```bash
docker ps
```

### 📜 Ver logs del backend

```bash
docker logs -f worker-redis-image-backend-1
```

### ⚙️ Ver logs de workers

```bash
docker logs -f worker-redis-image-worker-1
```

---

## 🌐 Acceso al Sistema

| Servicio | URL |
|---|---|
| Frontend | http://localhost:5500 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

---

## 📡 Flujo del Sistema

1. Usuario sube una imagen
2. Backend genera un `job_id`
3. Redis almacena la tarea en cola
4. Worker consume la tarea
5. Imagen procesada
6. Estado cambia a `completed`
7. Frontend actualiza automáticamente

---

## 📈 Escalabilidad

```bash
docker compose up -d --scale worker=10
```

---

## 🧠 Conceptos Aplicados

- Arquitectura distribuida
- Procesamiento asíncrono
- Microservicios
- Docker
- Escalabilidad horizontal
- Colas de mensajes
- Cloud Computing

---

## ✅ Estado del Proyecto

- ✔ Backend funcional
- ✔ Redis operativo
- ✔ Workers escalables
- ✔ Frontend conectado
- ✔ Procesamiento distribuido

---

## 👨‍💻 Autor

**Javier N. López Prudencio**
