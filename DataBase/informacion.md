# 📋 Comparación entre Diagrama ER y Estructura de Base de Datos

Este documento detalla las diferencias y coincidencias entre el diagrama entidad-relación (ER) proporcionado y la estructura real observada en la base de datos PostgreSQL `trabajo2paralela`.

---

## ✅ Coincidencias entre Diagrama y Base de Datos

### 🧬 Tabla `species`

- **Coincidencias:**
  - `code`
  - `name`
  - `created`
  - `updated`
- **Diferencia:**
  - En el diagrama, `code` parece ser la clave primaria (`pk`), pero en la base de datos se utiliza una columna `id` (`integer`) como **clave primaria real**.

---

### 🚻 Tabla `genders`

- **Coincidencias:**
  - `code`
  - `name`
  - `created`
  - `updated`
- **Diferencia:**
  - En lugar de usar `code` como `pk`, la base usa un campo `id` como **clave primaria**.

---

### 🧱 Tabla `strata`

- **Coincidencias:**
  - `code`
  - `name`
  - `description`
  - `created`
  - `updated`
- **Diferencia:**
  - Al igual que las otras tablas, la base de datos usa un campo `id` como **clave primaria**, aunque en el diagrama no se muestra.

---

### 👤 Tabla `persons`

- **Coincidencias:**
  - `species_fk`
  - `strata_fk`
  - `gender_fk`
  - `rut`
  - `birthdate`
  - `firstname`
  - `lastname`
  - `created`
  - `updated`
- **Diferencia:**
  - En la base se agrega una columna `id` como **clave primaria**, no presente en el diagrama.

---

## ⚠️ Tabla adicional no presente en el diagrama

### 🏰 Tabla `eldoria`

- **No está en el diagrama ER.**
- **Campos observados:**
  - `identificador`
  - `especie`
  - `genero`
  - `nombre`
  - `apellido`
  - `fecha_nacimiento`
  - `cp_origen`
  - `cp_destino`
- **Posible función:** tabla de staging o para carga de datos externa.

---

## 📝 Conclusión

- El modelo ER representa correctamente la lógica de relaciones y columnas, pero **en la implementación real se usa una columna `id` (tipo `integer`) como clave primaria** en todas las tablas principales (`species`, `genders`, `strata`, `persons`).
- Esta decisión es común para facilitar relaciones y generar claves automáticas.
- La tabla `eldoria` no forma parte del modelo relacional principal, y probablemente se usa como apoyo para cargas masivas o staging temporal.
