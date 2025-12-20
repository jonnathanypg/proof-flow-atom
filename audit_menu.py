import os
import sys
import subprocess
import time

def clear_screen():
    # Detecta el sistema operativo para limpiar la pantalla correctamente
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("="*85)
    print("🚀  UDF TECHNICAL AUDIT TOOL - INTERACTIVE CLI")
    print("="*85)

def get_input(prompt, default=None):
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def run_menu():
    while True:
        clear_screen()
        print_header()
        
        print("\n📝 CONFIGURACIÓN DE CORREOS")
        print("-" * 30)
        admin_email = get_input("  🔹 Correo Administrador (Para recibir reportes)", default="jonnathanyosue@gmail.com")
        student_email = get_input("  🔹 Correo Estudiante (Para simular reserva)", default="student.test@example.com")
        
        print("\n⚙️  SELECCIONE EL MODO DE AUDITORÍA")
        print("-" * 30)
        print("  [1] ✅ MODO NORMAL (Simulación Exitosa)")
        print("  [2] ⚠️  MODO FALLO (Prueba de Contingencia T07)")
        print("  [Q] 🚪 Salir")
        
        choice = input("\n👉 Opción: ").strip().lower()
        
        if choice == 'q':
            print("\n👋 ¡Hasta luego!")
            break
            
        cmd = [sys.executable, "atom_tests.py"]
        
        # Agregamos los argumentos dinámicos
        cmd.extend(["--admin", admin_email])
        cmd.extend(["--student", student_email])
        
        if choice == '2':
            cmd.append("--fail")
        elif choice != '1':
            print("\n❌ Opción no válida. Intente de nuevo.")
            time.sleep(1.5)
            continue
            
        print("\n" + "="*85)
        print(f"🔄 EJECUTANDO AUDITORÍA... (Modo: {'FALLO' if choice == '2' else 'NORMAL'})")
        print("="*85 + "\n")
        
        # Ejecutamos el script y mostramos la salida en tiempo real
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            print(f"\n❌ Error al ejecutar el script: {e}")
            
        input("\n✅ Presione ENTER para volver al menú...")

if __name__ == "__main__":
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario.")
        sys.exit(0)
