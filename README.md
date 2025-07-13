# TrabajoRest - API de Otro Mundo

Trabajo Número 2 de Computación Paralela 1-2025  
Profesor: Sebastián Salazar Molina  
Entrega: 15 de julio de 2025

---

## Descripción

API REST que replica la especificación del endpoint [https://api.sebastian.cl/isekai/swagger-ui/index.html](https://api.sebastian.cl/isekai/swagger-ui/index.html).  

Permite consultar:  

- Estratos sociales disponibles  
- Especies disponibles  
- Géneros disponibles  
- Estadísticas de conteo  
- Estadísticas de edad

---

## Tecnologías usadas

- **Python 3.11.9**  
- **FastAPI 0.116.1**  
- **psycopg2 2.9.10** (PostgreSQL driver)  
- **uvicorn 0.35.0** (Servidor ASGI)  
- **python-dotenv 1.1.1** (Manejo de variables de entorno)  
- **Base de datos:** PostgreSQL 16.9

Herramientas usadas para desarrollo y prueba:  

- pgAdmin  
- DBeaver

---

## Estado del proyecto

Proyecto realizado como trabajo académico para la asignatura Computación Paralela y Distribuida.  

Fecha de entrega original: 13 de julio de 2025  
Fecha de entrega actualizada: 15 de julio de 2025

---

## Requisitos previos

- Python 3.11.9  
- PostgreSQL 16.9 (conexión remota al host 159.223.200.213)  
- Dependencias listadas en `requirements.txt` o instalables con:

```bash
pip install fastapi psycopg2 uvicorn python-dotenv
````

---

## Instalación

1. Clonar el repositorio:

```bash
git clone <url-del-repo>
cd TrabajoRest
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno copiando y editando el archivo de ejemplo:

```bash
cp API/ejemplo.env .env
# Edita .env con los datos de conexión a tu base de datos PostgreSQL
```

4. Correr el servidor localmente:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Configuración

El archivo `.env` contiene variables para la conexión a la base de datos PostgreSQL:

* Host
* Puerto
* Usuario
* Contraseña
* Nombre de la base de datos

---

## Uso básico

La API correrá en [http://localhost:8000](http://localhost:8000) (o la IP/puerto configurados).

---

## Documentación de la API

La documentación interactiva está disponible en:

```
http://localhost:8000/docs
```

![Swagger UI](/Images/API.png)

---

## Ejemplos de peticiones

Consulta de estratos sociales:

```bash
curl -X GET "http://localhost:8000/isekai/v1/info/strata" -H "accept: application/json"
```

---

## Autenticación

Actualmente, la API no implementa ningún mecanismo de autenticación.

---

## Manejo de errores

Ejemplos de respuestas de error:

* Código 404 (No encontrado):

```json
{
  "detail": "No se encontró código 'HUM' en species"
}
```

* Código 422 (Error de validación):

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "gender_code"],
      "msg": "Field required"
    }
  ]
}
```

---

## Testing

(Agregar instrucciones para correr tests, si los tienes)

---

## Despliegue

(Agregar instrucciones si aplica para desplegar en un servidor)

---

## Contribución

* Realizar pull requests contra la rama `main` o `develop` (según convenga)
* Mantener formato y estilo PEP8 para Python
* Documentar cualquier cambio relevante

---

## Licencia

(Incluir tipo de licencia, ej. MIT, GPL, etc.)

---

## Contacto / Soporte

Para dudas o soporte, contactar a:
Sebastián Salazar Molina
[email@universidad.cl](mailto:email@universidad.cl) (poner email real)

---

## Contexto del trabajo

Este proyecto replica la API original especificada en [https://api.sebastian.cl/isekai/swagger-ui/index.html](https://api.sebastian.cl/isekai/swagger-ui/index.html), implementando los mismos endpoints, parámetros y respuestas.

El proyecto se desarrolla para la asignatura Computación Paralela y Distribuida, utilizando paralelismo y buenas prácticas para mejorar la eficiencia.

---

```

---

Si quieres, te ayudo a dejarlo listo con links reales, agregar ejemplos de tests o la parte de despliegue. ¿Qué te parece?
```
