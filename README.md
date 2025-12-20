# 🎓 UDF Technical Audit Tool (Interactive CLI)
**Autor:** Jonnathan Peña | **Desarrollado para:** ATOM (Prueba AI Specialist) | **Año:** 2025

Este proyecto implementa una herramienta de auditoría automatizada en Python para validar la integridad y robustez de un flujo conversacional exportado de **Atom Flowbuilder**. Incluye una interfaz de línea de comandos (CLI) interactiva para facilitar la ejecución de pruebas en diferentes entornos.

---

## � Inicio Rápido

El proyecto incluye scripts "inteligentes" que detectan tu sistema operativo, crean el entorno virtual (`venv`) e instalan las dependencias automáticamente.

### 🍎 macOS / � Linux
Abre tu terminal en la carpeta del proyecto y ejecuta:
```bash
./test_atom.sh
```

### 🪟 Windows
Haz doble clic en el archivo `test_atom.bat` o ejecútalo desde CMD/PowerShell:
```cmd
test_atom.bat
```

> **Nota:** La primera ejecución puede tardar unos segundos mientras se instala `requests`. Las siguientes serán instantáneas.

---

## 🎮 Interfaz Interactiva (CLI)

Al iniciar, verás un menú que te guiará en el proceso:

### 1. Configuración de Correos 📧
El sistema te pedirá dos correos (puedes presionar ENTER para usar los valores por defecto):
- **Admin Email:** Recibe los reportes de error y alertas de soporte.
- **Student Email:** Se usa para simular la reserva en el calendario.

### 2. Modos de Auditoría ⚙️
Selecciona qué escenario deseas auditar:

*   **[1] ✅ MODO NORMAL:**
    *   Simula un flujo exitoso donde la API funciona correctamente.
    *   Verifica: Agendamiento en Google Calendar, Generación de PDF y envío de Correos.

*   **[2] ⚠️  MODO FALLO (Prueba de Contingencia T07):**
    *   Simula una caída del servicio de Google Calendar.
    *   **Objetivo:** Verificar que el sistema active el **Plan B** (PDF de respaldo sin evento) y notifique a soporte.

---

## 🧪 Cobertura de Pruebas (T00 - T07)

El script `atom_tests.py` ejecuta 8 casos de prueba críticos de forma secuencial:

| Test ID | Nombre | Descripción y Validación |
| :--- | :--- | :--- |
| **T00** | **Validación de Prompts** | Analiza la integridad de los *Smartons*. <br>• **#1 Asesor:** Busca "Extracción de datos", "Base de conocimiento" y **Ejemplos de Carreras**. <br>• **#2 Agendar:** Verifica instrucciones mandatorias y pasos críticos (Hora). <br>• **#3 Post-Venta:** Verifica contexto y **Ejemplos Post-Venta**. |
| **T01** | **Oferta Académica** | Verifica que el bot tenga conocimiento sobre carreras. Busca keywords como *"Carrera"*, *"Programas"*, *"Ingeniería"*. |
| **T02** | **Requisitos** | Valida si el flujo responde a consultas de admisión (cédula, título, etc.). |
| **T03** | **Agendamiento E2E** | (Solo Modo Normal) Prueba la integración real con Google Calendar y Drive (PDF). |
| **T04** | **Captura de Contexto** | Confirma que variables críticas (`first_name`, `email`, `carrera_interes`) se guarden en memoria. |
| **T05** | **Cambio de Opinión** | Simula un usuario cambiando de carrera a mitad del flujo y valida la actualización de la variable. |
| **T06** | **Memoria** | Verifica que el bot mantenga el hilo de la conversación sin repetirse. |
| **T07** | **Plan B (Resiliencia)** | (Solo Modo Fallo) Valida la respuesta ante errores: <br>✅ Detecta fallo controlado <br>✅ Genera PDF de contingencia <br>✅ Alerta a Soporte. |

---

## 📂 Estructura del Proyecto

*   `audit_menu.py`: Script principal que maneja la interfaz de usuario.
*   `atom_tests.py`: Núcleo lógico de las pruebas y validaciones.
*   `test_atom.sh` / `test_atom.bat`: Launchers inteligentes multiplataforma.
*   `requirements.txt`: Lista de dependencias (principalmente `requests`).
*   `udf_flow_metadata.json`: Archivo fuente del flujo (Entrada de la auditoría).

---

## 📊 Diagrama de Flujo

```mermaid
flowchart TD
    A("🚀 Launcher (.sh / .bat)") --> B["🖥️ audit_menu.py"]
    B --> C{"⚙️ Selección de Modo"}
    
    C -- "Modo Normal" --> D["atom_tests.py"]
    C -- "Modo Fallo" --> E["atom_tests.py --fail"]
    
    D --> F["🔍 T00-T06: Validaciones Estáticas"]
    E --> F
    
    F --> G{"📡 T03/T07: Integración API"}
    
    G -- "Normal" --> H["✅ Agendamiento OK<br>(Calendar + PDF)"]
    G -- "Fallo Simulado" --> I["⚠️ Plan B Activado<br>(PDF Respaldo + Alerta)"]
```

## 📊 Como Probamos la API de Google Apps Script

```mermaid
flowchart TD
    A["🚀 Inicio: atom_tests.py"] --> B{"📂 Lectura de udf_flow_metadata.json"}
    
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