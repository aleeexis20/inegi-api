# Práctica Integradora (Examen): Arquitectura Cloud para BI

Este proyecto migra un conjunto de datos normalizado del INEGI hacia una arquitectura en la nube, consumiéndolo a través de una API RESTful y visualizándolo en Power BI.

## 🛠️ Herramientas Utilizadas
* **Base de Datos:** Supabase (PostgreSQL)
* **Backend/API:** Python (Flask)
* **Hosting:** PythonAnywhere
* **Visualización (BI):** Power BI Desktop
* **Validación de API:** Postman

## 🚀 Pasos de la Práctica (Documentación)

### Paso 1: Migración a la Nube (Supabase)
Se modeló físicamente la base de datos a partir de un Excel normalizado, creando tablas relacionales y cargando los datos correspondientes en PostgreSQL.


### Paso 2 y 3: Desarrollo y Despliegue de la API (PythonAnywhere)
Se desarrolló una API en Flask con los siguientes endpoints públicos:
* **Catálogo General:** `GET https://aleeexis.pythonanywhere.com/api/unidades`
* **Consulta por ID:** `GET https://aleeexis.pythonanywhere.com/api/unidades/<id>` 
* **Buscador por Nombre:** `GET https://aleeexis.pythonanywhere.com/api/unidades/buscar?nombre=<texto>`
* **KPI Estatal:** `GET https://aleeexis.pythonanywhere.com/api/estadisticas/total_por_estado`
* **Filtros Múltiples:** `GET https://aleeexis.pythonanywhere.com/api/unidades/filtro?estado=<X>&actividad=<Y>`
* **Perfil Completo (Anidado):** `GET https://aleeexis.pythonanywhere.com/api/unidades/<id>/perfil_completo` 
* **Búsqueda Geoespacial:** `GET https://aleeexis.pythonanywhere.com/api/unidades/cercanas?lat=<X>&lon=<Y>&radio=<Z>` 

*Nota: El código fuente en este repositorio incluye documentación detallada por sección de acciones.*

### Paso 4: Visualización (Business Intelligence)
Se conectó Power BI directamente a la API web extrayendo los JSON. El dashboard incluye:
* 3 KPIs principales (Total de Establecimientos, Municipios, Sectores).
* Mapa interactivo validando calidad de datos geográficos.
* Gráfico de barras y distribución por anillos.
* Filtros interactivos por Municipio, Categoría y Búsqueda por Nombre.



### EJEMPLOS DE CONSULTA RAPIDA

**1. Catálogo General**
*   **Qué busca:** Muestra una lista general con un límite de 1000 registros.
*   **Enlace:** [https://aleeexis.pythonanywhere.com/api/unidades](https://aleeexis.pythonanywhere.com/api/unidades)

**2. Consulta por ID**
*   **Qué busca:** Trae la información básica exclusivamente de la unidad económica con el ID interno `963`.
*   **Enlace:** [https://aleeexis.pythonanywhere.com/api/unidades/963](https://aleeexis.pythonanywhere.com/api/unidades/963)

**3. Buscador por Nombre**
*   **Qué busca:** Encuentra todos los negocios que incluyan la palabra `FRUTAS` en su nombre comercial.
*   **Enlace:** [https://aleeexis.pythonanywhere.com/api/unidades/buscar?nombre=FRUTAS](https://aleeexis.pythonanywhere.com/api/unidades/buscar?nombre=FRUTAS)

**4. KPI Estatal**
*   **Qué busca:** Ejecuta una agrupación matemática que devuelve el conteo total de negocios registrados por cada estado.
*   **Enlace:** [https://aleeexis.pythonanywhere.com/api/estadisticas/total_por_estado](https://aleeexis.pythonanywhere.com/api/estadisticas/total_por_estado)

**5. Filtros Múltiples**
*   **Qué busca:** Filtra estrictamente los negocios que se ubican en el estado de `AGS` (Aguascalientes) Y que pertenecen al código de actividad económica `114119`.
*   **Enlace:** [https://aleeexis.pythonanywhere.com/api/unidades/filtro?estado=AGS&actividad=114119](https://aleeexis.pythonanywhere.com/api/unidades/filtro?estado=AGS&actividad=114119)

**6. Perfil Completo (Anidado)**
*   **Qué busca:** Trae el JSON complejo con toda la información detallada (contacto, vialidad, coordenadas) de la unidad con el ID `963`.
*   **Enlace:** [https://aleeexis.pythonanywhere.com/api/unidades/963/perfil_completo](https://aleeexis.pythonanywhere.com/api/unidades/963/perfil_completo)

**7. Búsqueda Geoespacial**
*   **Qué busca:** Traza un radio de `10` kilómetros alrededor de las coordenadas ingresadas (pertenecientes a Ensenada) y devuelve los negocios que se encuentran dentro de esa zona.
*   **Enlace:** [https://aleeexis.pythonanywhere.com/api/unidades/cercanas?lat=31.8667&lon=-116.5964&radio=10](https://aleeexis.pythonanywhere.com/api/unidades/cercanas?lat=31.8667&lon=-116.5964&radio=10)