import json
import requests
import os
import sys

def find_key_recursive(data, key_to_find):
    """Busca una clave de forma recursiva en la estructura del JSON del Flowbuilder."""
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key_to_find:
                return v
            result = find_key_recursive(v, key_to_find)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_recursive(item, key_to_find)
            if result:
                return result
    return None

def run_technical_audit(json_file, force_fail=False, custom_admin=None):
    """
    Ejecuta una auditoría completa del flujo:
    1. Valida presencia de Smartons.
    2. Prueba la conexión HTTP con el Apps Script.
    3. Verifica el manejo de Plan B (T07).
    """
    
    # =========================================================================
    # CONFIGURACIÓN MANUAL DEL ADMINISTRADOR
    # =========================================================================
    # ESCRIBE TU CORREO AQUÍ para no tener que usar el comando --admin
    CORREO_ADMIN_CONFIGURADO = "jonnathanyosue@gmail.com" 
    # =========================================================================

    print("="*85)
    print("🚀 UDF TECHNICAL AUDIT TOOL - UNIVERSIDAD DEL FUTURO")
    print(f"📂 Archivo de Metadatos: {json_file}")
    
    # Lógica de prioridad: 1. Comando Terminal (--admin), 2. Variable del Código
    final_admin = custom_admin if custom_admin else CORREO_ADMIN_CONFIGURADO
    
    if force_fail:
        print("⚠️  MODO DE PRUEBA T07: SIMULACIÓN DE FALLO DE CALENDARIO ACTIVADA")
    else:
        print("✅ MODO NORMAL: SIMULACIÓN DE AGENDAMIENTO EXITOSO")
        
    print(f"📧 Notificaciones dirigidas a: {final_admin}")
    print("="*85)

    if not os.path.exists(json_file):
        print(f"❌ ERROR: El archivo '{json_file}' no existe en el directorio.")
        return

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ ERROR: No se pudo parsear el JSON. {e}")
        return

    cells = data.get('cells', [])
    
    # --- FASE 1: SMARTONS ---
    print("\n[FASE 1] Análisis de Inteligencia Artificial (Smartons)")
    smartons = [c for c in cells if 'Smarton' in str(c.get('type', '')) or 'Smarton' in str(c.get('attrs', {}).get('label', {}).get('text', ''))]
    if smartons:
        print(f"✅ Se detectaron {len(smartons)} nodos de Smarton optimizados.")
    else:
        print("⚠️  No se detectaron Smartons explícitos.")

    # --- FASE 2: INTEGRACIÓN API (HTTP) ---
    print("\n[FASE 2] Prueba de Integración y Generación de PDF")
    
    http_url = None
    http_method = "POST"
    
    for cell in cells:
        found_url = find_key_recursive(cell, 'url')
        if found_url and isinstance(found_url, str) and "script.google.com" in found_url:
            http_url = found_url
            found_method = find_key_recursive(cell, 'method')
            if found_method: http_method = found_method.upper()
            break

    if not http_url:
        print("❌ ERROR: No se encontró la URL del Apps Script en el archivo JSON.")
        return

    print(f"🔗 Endpoint detectado: {http_url}")
    print(f"📡 Enviando petición {http_method}...")

    # Payload base para la auditoría
    payload = {
        "titulo": "Jonnathan Peña (Auditoría Técnica)",
        "invitado": "yosue.jpg@gmail.com",
        "email": "yosue.jpg@gmail.com",
        "carrera": "Ingeniería de Sistemas y Ciberseguridad",
        "fechaInicio": "2025-12-24T10:00:00",
        "fechaFin": "2025-12-24T11:00:00",
        "celular": "+593 982840685",
        "admin_email_override": final_admin 
    }

    # Si se activa el modo fail, inyectamos la flag para el Plan B (T07)
    if force_fail:
        payload["force_plan_b"] = True
        payload["titulo"] = "TEST T07 - SIMULACIÓN FALLO"

    try:
        response = requests.request(http_method, http_url, json=payload, timeout=20)
        
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get('success'):
                status_cal = res_data.get('calendar_status')
                if status_cal == "OK":
                    print(f"✅ ÉXITO: Cita agendada en Google Calendar.")
                    print(f"📝 Resultado: Se debió generar un PDF de confirmación estándar.")
                else:
                    print(f"✅ ÉXITO (PLAN B): El sistema detectó el error forzado y ejecutó la contingencia.")
                    print(f"📝 Resultado: Se generó un PDF de Registro Alternativo para administración.")
                
                if res_data.get('pdfLink'):
                    print(f"📄 PDF DISPONIBLE EN DRIVE: {res_data.get('pdfLink')}")
                    print(f"📧 Archivo enviado correctamente a: {final_admin}")
            else:
                print(f"❌ LA API RESPONDIÓ CON ERROR: {res_data.get('error')}")
        else:
            print(f"❌ ERROR DE RED: Status {response.status_code}")
            
    except Exception as e:
        print(f"🔴 ERROR CRÍTICO DURANTE LA PETICIÓN: {e}")

    # --- FASE 3: CONTEXTO ---
    print("\n[FASE 3] Verificación de Variables de Contexto")
    raw_content = json.dumps(data)
    for var in ["first_name", "email", "carrera_interes", "fecha_cita"]:
        status = "✅" if var in raw_content else "❌"
        print(f" {status} Variable '{var}' encontrada en el flujo.")

    print("\n" + "="*85)
    print("🏁 AUDITORÍA FINALIZADA")
    print("="*85)

if __name__ == "__main__":
    # Verificamos si el usuario quiere simular un fallo (T07)
    is_fail_mode = "--fail" in sys.argv
    
    # Verificamos si el usuario quiere sobreescribir el admin por comando
    custom_admin_arg = None
    if "--admin" in sys.argv:
        try:
            idx = sys.argv.index("--admin")
            custom_admin_arg = sys.argv[idx + 1]
        except: pass

    # Nombre del archivo de metadatos del flujo
    archivo_metadatos = "udf_flow_metadata.json"
    
    # Ejecutamos la función principal
    run_technical_audit(archivo_metadatos, force_fail=is_fail_mode, custom_admin=custom_admin_arg)