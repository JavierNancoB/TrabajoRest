# TrabajoRest - API de Otro Mundo

<p>
  ![Logo UTEM](./Images/Logo_utem.jpg)
</p>

Trabajo Número 2 de Computación Paralela 1-2025  
Profesor: Sebastián Salazar Molina  
Entrega: 15 de julio de 2025

**Estudiante 1:** Javier Nanco Becerra  
**Estudiante 2:** Aranza Sue Diaz  
**Estudiante 3:** Ignacio Baeza Villaroel

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

| Tecnología        | Versión    | Descripción                                 | Repositorio / Web                              |
|-------------------|------------|---------------------------------------------|-----------------------------------------------|
| Python            | 3.11.9     | Lenguaje de programación                     | [python.org](https://www.python.org/)         |
| FastAPI           | 0.116.1    | Framework para APIs web                       | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| psycopg2          | 2.9.10     | Driver PostgreSQL para Python                 | [psycopg.org](https://www.psycopg.org/)       |
| uvicorn           | 0.35.0     | Servidor ASGI para correr FastAPI             | [www.uvicorn.org](https://www.uvicorn.org/)   |
| python-dotenv     | 1.1.1      | Manejo de variables de entorno                 | [pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/) |
| PostgreSQL        | 16.9       | Sistema gestor de base de datos relacional    | [postgresql.org](https://www.postgresql.org/) |

Herramientas para desarrollo y prueba:

| Herramienta       | Descripción                     | Web                                           |
|-------------------|---------------------------------|-----------------------------------------------|
| pgAdmin           | Gestión visual de bases de datos | [pgadmin.org](https://www.pgadmin.org/)       |
| DBeaver           | Cliente universal para DB         | [dbeaver.io](https://dbeaver.io/)              |

---

## Estado del proyecto

Proyecto realizado como trabajo académico para la asignatura Computación Paralela y Distribuida.  

Fecha de la Última Actualización: 13-07-2025  
Fecha de entrega original: 13 de julio de 2025  
Fecha de entrega actualizada: 15 de julio de 2025

---

## Requisitos previos

- Python 3.11.9  
- PostgreSQL 16.9 (conexión remota al host 159.223.200.213 para el archivo de base de datos original)  
- Dependencias listadas en `requirements.txt` o instalables con:

```bash
pip install fastapi psycopg2 uvicorn python-dotenv
```

1. Clonar el repositorio:

```bash
git clone https://github.com/JavierNancoB/TrabajoRest
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

- Host
- Puerto
- Usuario
- Contraseña
- Nombre de la base de datos

---

## Uso básico

La API correrá en [http://localhost:8000](http://localhost:8000) (o la IP/puerto configurados).

---

## Documentación de la API

Al momento de estar ejecutando la API, la documentación interactiva está disponible en el siguiente enlace:
[http://localhost:8000/docs](http://localhost:8000/docs)

<p align="center">
  <img src="/Images/API.png" alt="Swagger UI" height="400px" />
</p>

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

- Código 404 (No encontrado):

```json
{
  "detail": "No se encontró código 'HUM' en species"
}
```

- Código 422 (Error de validación):

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

## Contribución

- Realizar pull requests contra la rama `main` o `develop` (según convenga)
- Mantener formato y estilo PEP8 para Python
- Documentar cualquier cambio relevante

---

## Licencia

[Ver licencia](./LICENSE)

---

## Contacto / Soporte

Para dudas o soporte, contactar a:
Javier Alonso Nanco Becerra
[jnanco@utem.cl](mailto:jnanco@utem.cl)

---

## Contexto del trabajo

Este proyecto replica la API original especificada en [https://api.sebastian.cl/isekai/swagger-ui/index.html](https://api.sebastian.cl/isekai/swagger-ui/index.html), implementando los mismos endpoints, parámetros y respuestas.

El proyecto se desarrolla para la asignatura Computación Paralela y Distribuida, utilizando paralelismo y buenas prácticas para mejorar la eficiencia.
