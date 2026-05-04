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

### Paso 4: Visualización (Business Intelligence)
Se conectó Power BI directamente a la API web extrayendo los JSON. El dashboard incluye:
* 3 KPIs principales (Total de Establecimientos, Municipios, Sectores).
* Mapa interactivo validando calidad de datos geográficos.
* Gráfico de barras y distribución por anillos.
* Filtros interactivos por Municipio, Categoría y Búsqueda por Nombre.
