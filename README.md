🎓 Validador Técnico de Flujo UDF (Atom Flow)
Este proyecto contiene una herramienta de automatización avanzada en Python diseñada por Jonnathan Peña como parte del ejercicio técnico solicitado por ATOM. Su objetivo es validar la integridad del archivo JSON exportado desde Atom Flowbuilder y verificar la resiliencia de la API de agendamiento (Caso T07).

📊 Diagrama de Flujo del Proceso de Auditoría

```
graph TD
    A[Inicio: Script autom_tests.py] --> B{Lectura de udf_flow_metadata.json}
    B -- Archivo OK --> C[Fase 1: Análisis de Smartons]
    B -- No existe --> X[Error: Detener Auditoría]
    C --> D[Fase 2: Identificación de Variables de Contexto]
    D --> E[Fase 3: Prueba de Integración HTTP]
    E --> F{¿Modo --fail activado?}
    F -- SI --> G[Envío payload con force_plan_b: true]
    F -- NO --> H[Envío payload estándar]
    G --> I[Recepción de Respuesta Plan B]
    H --> J[Recepción de Confirmación Calendar]
    I --> K[Generación de Reporte Final ✅]
    J --> K
```

🛠️ Requisitos Previos
Python 3.10+ instalado en tu sistema

Archivo de metadatos udf_flow_metadata.json en la raíz del proyecto

🚀 Configuración del Entorno
1. Crear y Activar el Entorno Virtual
bash
# Crear entorno
```
python3 -m venv venv
```

# Activar en macOS/Linux:
```
source venv/bin/activate
```

# Activar en Windows:
```
.\venv\Scripts\activate
```

2. Instalar Dependencias
Instalamos requests para la comunicación con la API de Google Apps Script:

```
pip3 install requests
```

🧪 Ejecución de las Pruebas
El script permite varios modos de ejecución para validar los criterios técnicos:

A. Prueba de Agendamiento Normal
Valida que el flujo detecte el calendario y cree la cita correctamente.

```
python3 autom_tests.py
```

B. Simulación de Error de Agendamiento (Caso T07 - Plan B)
Fuerza al backend a ignorar el calendario y activar la contingencia (PDF de emergencia).

```
python3 autom_tests.py --fail
```

C. Cambio de Correo Administrador
Recibir el PDF de prueba en un correo distinto al configurado por defecto:

```
python3 autom_tests.py --admin tu-correo-aqui@gmail.com
```

📝 Configuración Interna
Dentro del archivo autom_tests.py, puedes modificar la variable global para configurar el correo administrador por defecto:


# Ubicación: Línea 33 aproximadamente
```
CORREO_ADMIN_CONFIGURADO = "tu-correo@ejemplo.com"
```

🔍 Criterios de Validación Técnica
Smartons IA: Verifica que el flujo use los componentes de IA optimizados

Contexto Persistente: Comprueba que variables como first_name, email y carrera_interes existan en la estructura

Resiliencia (Plan B): Valida que ante un error, el sistema retorne un pdfLink y ejecute la lógica de notificación administrativa

Desarrollado por: Jonnathan Peña
Para: ATOM - Prueba AI Specialist
Año: 2025