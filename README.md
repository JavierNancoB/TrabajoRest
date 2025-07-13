# TrabajoRest - API de Otro Mundo

<p align="left">
  <img src="/Images/Logo_utem.jpg" alt="Utem Logo" height="200px" />
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
- PostgreSQL 16.9 (conexión remota al host para el archivo de base de datos original)  
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

4. Correr el servidor localmente (modo desarrollo)

> **Nota:** Este comando es para desarrollo local. Usa `--reload` para que el servidor se reinicie automáticamente al detectar cambios en el código. No se recomienda para producción.

```bash
cd API
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

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

<p align="left">
  <img src="/Images/Diagrama.png" alt="Diagrama" height="600px" />
</p>

## Paralelismo y optimización

Para mejorar la eficiencia de las consultas a la base de datos PostgreSQL, se implementó paralelismo en la obtención de claves foráneas (FK) necesarias para los filtros de los endpoints de estadísticas, especificamente en el servicio de estadisticas de la API, se encuentras aquí [stats_service.py](./API/services/stats_service.py).

En particular, en los endpoints que retornan estadísticas de conteo y edad, se utiliza `concurrent.futures.ThreadPoolExecutor` para paralelizar las consultas que buscan los valores de clave primaria asociados a los códigos de estrato (`strata_code`), especie (`species_code`) y género (`gender_code`).

Esto permite realizar simultáneamente las consultas a las tablas `strata`, `species` y `genders`, reduciendo el tiempo de espera total y mejorando el rendimiento global de la API.

El código clave para esta paralelización es la función `get_fks_parallel` que ejecuta en paralelo las consultas de FK, utilizando un cache (`FK_CACHE`) para evitar consultas repetidas y acelerar aún más la respuesta.

Esta estrategia de paralelismo resulta especialmente beneficiosa cuando la API debe atender múltiples solicitudes concurrentes o cuando las consultas de FK tardan un tiempo considerable, logrando un servicio más eficiente y rápido para el usuario.

## Resultados Esperados

Al completar la configuración y ejecutar el servidor, el usuario podrá consultar los datos definidos en la base de datos mediante endpoints claros y eficientes, con tiempos de respuesta optimizados gracias al paralelismo y uso de caché implementados.

En condiciones ideales, con una base de datos cargada con aproximadamente 100 millones de filas, se espera que:

El endpoint de estadísticas de conteo (/count) responda en menos de 20 segundos.

El endpoint de estadísticas de edad (/age-stats) lo haga en menos de 40 segundos.

Estas cifras representan los objetivos de rendimiento del sistema en escenarios de alta carga.

> **Nota:** Actualmente, la base de datos utilizada no contiene la cantidad total de registros requerida (100 millones), por lo que no es posible realizar una evaluación empírica completa de dichos tiempos de respuesta. Sin embargo, la arquitectura propuesta y las técnicas aplicadas están diseñadas para escalar adecuadamente bajo dichas condiciones.

Se espera que este enfoque facilite el consumo de datos por aplicaciones cliente, manteniendo una arquitectura escalable, modular y eficiente, apta para extenderse o adaptarse a escenarios de producción reales.

## Documentación de la API

Al momento de estar ejecutando la API, la documentación interactiva está disponible en el siguiente enlace:
[http://localhost:8000/docs](http://localhost:8000/docs).

En la Siguiente imagnese puede visualizar lo que verá el usuario cuando entre al enlace. Aqui se pueden probar todas los [ENDPOINTS](https://www.icm.es/2021/06/15/que-son-endpoints/) configurados.

<p align="center">
  <img src="/Images/API.png" alt="Swagger UI" height="400px" />
</p>

Los ENDPOINTS se dividen en dos grupos principales. Primero esta el desplegable de la información base y despues el desplegable de Estadisticas.

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
