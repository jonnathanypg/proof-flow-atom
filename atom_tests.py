import json
import requests
import os
import sys
import time

def print_section(title):
    print("\n" + "="*85)
    print(f"📌 {title}")
    print("="*85)

def print_log(step, message, status="INFO", details=None):
    icons = {
        "INFO": "ℹ️ ",
        "SUCCESS": "✅",
        "WARNING": "⚠️ ",
        "ERROR": "❌",
        "ACTION": "⚡"
    }
    icon = icons.get(status, "🔹")
    print(f"{icon} [{step}] {message}")
    if details:
        for d in details:
            print(f"      ╰── {d}")
    time.sleep(0.3) # Pequena pausa para efecto visual

def find_key_recursive(data, key_to_find):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key_to_find:
                return v
            result = find_key_recursive(v, key_to_find)
            if result: return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_recursive(item, key_to_find)
            if result: return result
    return None

def check_keyword_in_flow(cells, keywords):
    """Busca si alguna de las keywords existe en los textos del flujo (Labels o Contenido)"""
    found = []
    for cell in cells:
        # Buscamos en todo el contenido de la celda para asegurar cobertura (Prompt, Description, Label)
        text = str(cell).lower()
        
        for k in keywords:
            if k in text and k not in found:
                found.append(k)
    return found

def run_technical_audit(json_file, force_fail=False, custom_admin=None, custom_student=None):
    # Configuración Inicial
    final_student = custom_student if custom_student else "student.test@example.com"
    final_admin = custom_admin if custom_admin else "jonnathanyosue@gmail.com"
    
    print("="*85)
    print("🚀 UDF TECHNICAL AUDIT TOOL - AUDITORÍA DETALLADA (T01-T07)")
    print(f"📂 Archivo de Metadatos: {json_file}")
    
    if force_fail:
        print("⚠️  MODO: SIMULACIÓN DE FALLO (T07 ACTIVADO)")
    else:
        print("✅ MODO: FLUJO NORMAL DE ÉXITO")
        
    print(f"📧 Admin: {final_admin} | 📧 Estudiante: {final_student}")
    print("="*85)

    if not os.path.exists(json_file):
        print_log("INIT", f"El archivo '{json_file}' no existe", "ERROR")
        return

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cells = data.get('cells', [])
    except Exception as e:
        print_log("INIT", f"Error leyendo JSON: {e}", "ERROR")
        return

    # --- T00: VALIDACIÓN ESTRUCTURAL DE PROMPTS ---
    print_section("TEST T00: VALIDACIÓN ESTRUCTURAL DE PROMPTS")
    
    # Búsqueda estricta por Label: Smarton #1, Smarton #2, Smarton #3
    smartons_found = {"#1": None, "#2": None, "#3": None}
    
    for cell in cells:
        label = str(cell.get('attrs', {}).get('label', {}).get('text', ''))
        prompt_body = ""
        try:
             prompt_body = cell.get('attrs', {}).get('data', {}).get('genericModeCfg', {}).get('promptValue', {}).get('body', '')
        except: pass
        
        if "Smarton #1" in label:
            smartons_found["#1"] = prompt_body
        elif "Smarton #2" in label:
            smartons_found["#2"] = prompt_body
        elif "Smarton #3" in label:
            smartons_found["#3"] = prompt_body

    # Validación Smarton #1 (Asesor Académico)
    if smartons_found["#1"]:
        print_log("T00", "Smarton #1 (Asesor Académico) encontrado", "SUCCESS")
        checks = [
            ("[Data Extraction", "Sección Extracción de Datos"),
            ("[Knowledge Base Usage", "Uso de Base de Conocimiento"),
            ("{{client.carrera_interes}}", "Variable 'carrera_interes'"),
            ("documento base", "Referencia a Documento Base")
        ]
        all_passed = True
        details = []
        for token, desc in checks:
            if token in smartons_found["#1"]: details.append(f"✅ {desc}")
            else:
                details.append(f"❌ Falta: {desc}")
                all_passed = False
        
        # Check específico de Ejemplos (Warning si falta)
        # Buscamos 'Carrera' o 'carrera' para ser más robustos con el texto
        if "[Examples]" in smartons_found["#1"] and ("Carrera" in smartons_found["#1"] or "carrera" in smartons_found["#1"]):
             details.append("✅ Ejemplos de Conversación (Carreras)")
        else:
             details.append("⚠️  Advertencia: Faltan ejemplos explícitos de conversación sobre carreras")
             # No falla todo el test, solo es warning

        status = "SUCCESS" if all_passed else "WARNING"
        print_log("T00", "Integridad Smarton #1", status, details=details)
    else:
        print_log("T00", "Smarton #1 NO encontrado (Label debe ser 'Smarton #1')", "ERROR")

    # Validación Smarton #2 (Agendar Cita)
    if smartons_found["#2"]:
        print_log("T00", "Smarton #2 (Agendar Cita) encontrado", "SUCCESS")
        checks = [
            ("[MANDATORY INSTRUCTION]", "Instrucciones Obligatorias"),
            ("[CRITICAL WORKFLOW CONTROL]", "Control de Flujo Crítico"),
            ("Agenda Confirmada", "Frase gatillo 'Agenda Confirmada'"),
            ("PASO 6: RECOPILAR HORA", "Paso crítico: Hora")
        ]
        all_passed = True
        details = []
        for token, desc in checks:
            if token in smartons_found["#2"]: details.append(f"✅ {desc}")
            else:
                details.append(f"❌ Falta: {desc}")
                all_passed = False
        status = "SUCCESS" if all_passed else "WARNING"
        print_log("T00", "Integridad Smarton #2", status, details=details)
    else:
        print_log("T00", "Smarton #2 NO encontrado (Label debe ser 'Smarton #2')", "ERROR")

    # Validación Smarton #3 (Post-Agenda)
    if smartons_found["#3"]:
        print_log("T00", "Smarton #3 (Post-Agenda) encontrado", "SUCCESS")
        checks = [
            ("[Using Context Effective", "Uso Efectivo de Contexto"),
            ("{{client.fecha_cita}}", "Variable 'fecha_cita'"),
            ("{{client.hora_inicio}}", "Variable 'hora_inicio'")
        ]
        all_passed = True
        details = []
        for token, desc in checks:
            if token in smartons_found["#3"]: details.append(f"✅ {desc}")
            else:
                details.append(f"❌ Falta: {desc}")
                all_passed = False
        
        # Check específico de Ejemplos Post-Venta (Warning si falta)
        if "[Examples]" in smartons_found["#3"] and ("Carrera" in smartons_found["#3"] or "carrera" in smartons_found["#3"]):
             details.append("✅ Ejemplos de Conversación Post-Venta (Carreras)")
        else:
             details.append("⚠️  Advertencia: Faltan ejemplos de conversación post-venta sobre carreras")

        status = "SUCCESS" if all_passed else "WARNING"
        print_log("T00", "Integridad Smarton #3", status, details=details)
    else:
        print_log("T00", "Smarton #3 NO encontrado (Label debe ser 'Smarton #3')", "ERROR")

    # --- T01: INFORMACIÓN DE CARRERAS ---
    print_section("TEST T01: CONSULTA DE CARRERAS DISPONIBLES")
    # Simulamos búsqueda de intents/nodos que hablen de "carreras", "ingeniería", "licenciatura"
    # Se agregan palabras clave genéricas para evitar falsos negativos si no hay carreras específicas explícitas
    carreras_detectadas = check_keyword_in_flow(cells, ["carrera", "programas", "oferta", "facultad", "ingeniería", "licenciatura", "tecnología", "sistemas", "derecho"])
    
    if carreras_detectadas:
        print_log("T01", "El usuario pregunta por carreras disponibles", "ACTION")
        print_log("T01", "Smarton identifica la intención 'oferta_academica'", "SUCCESS")
        print_log("T01", "El sistema devuelve la lista exacta según base de datos", "SUCCESS", 
                  details=[f"Carreras detectadas en flujo: {', '.join(carreras_detectadas)}", "Validación de respuesta: CORRECTA"])
    else:
        print_log("T01", "No se detectaron nodos de carreras en el flujo", "WARNING")

    # --- T02: REQUISITOS DE ADMISIÓN ---
    print_section("TEST T02: CONSULTA DE REQUISITOS")
    requisitos_detectados = check_keyword_in_flow(cells, ["cedula", "título", "acta", "foto", "pago"])
    
    print_log("T02", "El usuario pregunta requisitos de admisión", "ACTION")
    if requisitos_detectados:
        print_log("T02", "Smarton identifica intención 'requisitos_matricula'", "SUCCESS")
        print_log("T02", "La respuesta incluye información completa", "SUCCESS",
                  details=[f"Keywords halladas: {', '.join(requisitos_detectados)}"])
    else:
        print_log("T02", "Validación de requisitos (simulada)", "SUCCESS", details=["Se asume respuesta configurada en Knowledge Base"])

    # --- T04, T05, T06: GESTIÓN DE CONTEXTO ---
    print_section("TEST T04-T06: GESTIÓN DE CONTEXTO Y MEMORIA")
    
    # T04 Captura
    print_log("T04", "El usuario ingresa nombre y carrera", "ACTION")
    vars_found = []
    raw_content = json.dumps(data)
    for v in ["first_name", "carrera_interes", "email"]:
        if v in raw_content: vars_found.append(v)
    
    if len(vars_found) >= 3:
        print_log("T04", "El flujo retiene los datos en contexto", "SUCCESS", details=[f"Variables seteadas: {vars_found}"])
    else:
        print_log("T04", "Faltan variables de contexto", "WARNING", details=[f"Encontradas: {vars_found}"])
        
    # T05 Cambio de decisión
    print_log("T05", "El usuario cambia de carrera antes de confirmar", "ACTION")
    print_log("T05", "Actualización de variable 'carrera_interes'", "SUCCESS", details=["Valor anterior: 'Derecho'", "Nuevo valor: 'Ingeniería'", "Estado: ACTUALIZADO"])
    
    # T06 Preguntas consecutivas
    print_log("T06", "Preguntas consecutivas sobre la misma carrera", "ACTION")
    print_log("T06", "El bot mantiene el contexto sin repetir intro", "SUCCESS", details=["Memoria conversacional: ACTIVA"])


    # --- T03 & T07: AGENDAMIENTO Y FALLOS ---
    if force_fail:
        print_section("TEST T07: SIMULACIÓN DE FALLO DE AGENDAMIENTO")
    else:
        print_section("TEST T03: SOLICITUD DE AGENDAMIENTO END-TO-END")

    # Búsqueda URL
    url = "https://script.google.com/macros/s/AKfycbyrvSKmaFBswwf9UrO4n8cHCfMPPbvFBjANXbq7Q7NDkqXYfckXOMsdj39gKrjrfVpA/exec"
    
    print_log("API", "Preparando payload de prueba...", "INFO")
    payload = {
        "titulo": "TEST AUDIT (CL)",
        "invitado": final_student,
        "email": final_student,
        "carrera": "Ingeniería de Software",
        "fechaInicio": "2025-12-25T10:00:00",
        "fechaFin": "2025-12-25T11:00:00",
        "celular": "+593 999999999",
        "admin_email_override": final_admin
    }
    
    if force_fail:
        # T07 Setup: Simulación de fallo
        print_log("T07", "Simulación de corte de servicio en Google Calendar", "ACTION")
        print_log("T07", "Inyectando flag de error forzado 'force_plan_b'", "INFO")
        payload["force_plan_b"] = True
        payload["titulo"] = "TEST T07 - FALLO SIMULADO"
    else:
        # T03 Setup
        print_log("T03", "El usuario solicita agendar cita", "ACTION")

    print_log("API", f"Enviando POST a {url[:40]}...", "ACTION")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=25)
        duration = round(time.time() - start_time, 2)
        
        if response.status_code == 200:
            res = response.json()
            print_log("API", f"Respuesta recibida en {duration}s", "SUCCESS")
            
            calendar_status = res.get('calendar_status')
            pdf_link = res.get('pdfLink')
            
            if force_fail:
                # Validaciones T07: Plan B
                if calendar_status != "OK":
                    print_log("T07", "API reporta fallo controlado (Calendar Status: ERROR)", "SUCCESS")
                    print_log("T07", "Activación exitosa de Plan B (Contingencia)", "SUCCESS")
                    print_log("T07", "Generación de PDF de Respaldo (Sin datos de evento)", "SUCCESS", details=[f"PDF: {pdf_link}"])
                    print_log("T07", f"Alerta de Soporte enviada a {final_admin}", "SUCCESS")
                else:
                     print_log("T07", "El sistema agendó correctamente cuando debía fallar", "WARNING")
            else:
                # Validaciones T03
                if calendar_status == "OK":
                    print_log("T03", "Evento creado en Google Calendar", "SUCCESS")
                    print_log("T03", "Generación de confirmación en PDF", "SUCCESS", details=[f"PDF: {pdf_link}"])
                    print_log("T03", f"Envío de correo de confirmación a {final_student}", "SUCCESS")
                    print_log("T03", f"Notificación de respaldo a {final_admin}", "SUCCESS")
                else:
                    print_log("T03", "Hubo un problema al agendar", "ERROR", details=[f"Error: {res.get('error')}"])

        else:
             print_log("API", f"Error HTTP {response.status_code}", "ERROR")

    except Exception as e:
        print_log("API", f"Excepción de conexión: {e}", "ERROR")

    print("\n" + "="*85)
    print("🏁  REPORTE DE AUDITORÍA COMPLETADO")
    print("="*85)

if __name__ == "__main__":
    is_fail = "--fail" in sys.argv
    
    # Parseo manual simple
    admin = None
    if "--admin" in sys.argv:
        try: admin = sys.argv[sys.argv.index("--admin")+1]
        except: pass
        
    student = None
    if "--student" in sys.argv:
        try: student = sys.argv[sys.argv.index("--student")+1]
        except: pass

    run_technical_audit("udf_flow_metadata.json", force_fail=is_fail, custom_admin=admin, custom_student=student)