🎓 Validador Técnico de Flujo UDF (Atom Flow)
Este proyecto contiene una herramienta de automatización avanzada en Python diseñada por Jonnathan Peña como parte del ejercicio técnico solicitado por ATOM. Su objetivo es validar la integridad del archivo JSON exportado desde Atom Flowbuilder y verificar la resiliencia de la API de agendamiento (Caso T07).

📊 Diagrama de Flujo del Proceso de Auditoría

```
flowchart TD
    A["🚀 Inicio: autom_tests.py"] --> B{"📂 Lectura de udf_flow_metadata.json"}
    
    B -- "✅ Archivo encontrado" --> C["Fase 1: Análisis de Smartons"]
    B -- "❌ No existe" --> X["⛔ Error: Detener Auditoría"]
    
    C --> D["Función find_key_recursive<br>en JSON"]
    D --> E{"🔍 URL HTTP encontrada?"}
    
    E -- "❌ No" --> Y["⛔ Error: Sin endpoint Apps Script"]
    E -- "✅ Sí" --> F["Fase 2: Integración API HTTP<br>Método: POST<br>Timeout: 20s"]
    
    F --> G{"⚙️ Modo de operación"}
    G -- "🟢 Normal (sin --fail)" --> H["📤 Payload estándar<br>Con admin_email_override"]
    G -- "🔴 --fail activado" --> I["📤 Payload con force_plan_b: true<br>Simulación T07"]
    
    H --> J["🔄 Petición a Google Apps Script"]
    I --> J
    
    J --> K{"📥 Estado respuesta HTTP"}
    K -- "✅ 200 OK" --> L["🔍 Análisis JSON respuesta"]
    K -- "❌ Error HTTP" --> M["🔴 Error de red"]
    
    L --> N{"🔎 Campo success = true?"}
    N -- "✅ Sí" --> O{"📊 Tipo de respuesta"}
    N -- "❌ No" --> P["❌ Error en API"]
    
    O -- "calendar_status: OK" --> Q["✅ ÉXITO: Cita agendada<br>📅 Google Calendar<br>📄 PDF generado"]
    O -- "calendar_status: ERROR<br>o force_plan_b activo" --> R["✅ ÉXITO (PLAN B)<br>📄 PDF contingencia<br>🔧 Notificación admin"]
    
    Q --> S["Fase 3: Verificación Variables<br>first_name, email, carrera_interes, fecha_cita"]
    R --> S
    P --> S
    M --> S
    
    S --> T["📊 Generación Reporte Final"]
    T --> U["🏁 Auditoría Completada<br>✅/❌ Resultados"]
    
    X --> U
    Y --> U

    style A fill:#4CAF50,stroke:#388E3C,color:white
    style X fill:#F44336,stroke:#D32F2F,color:white
    style Y fill:#F44336,stroke:#D32F2F,color:white
    style U fill:#2196F3,stroke:#1976D2,color:white
    style I fill:#FF9800,stroke:#F57C00,color:black
    style Q fill:#8BC34A,stroke:#689F38,color:black
    style R fill:#FFC107,stroke:#FFA000,color:black
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