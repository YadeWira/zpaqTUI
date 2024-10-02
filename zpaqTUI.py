import os
import subprocess
import msvcrt
import shutil  # Importar shutil para eliminar directorios no vacíos
import sys  # Importar sys para acceder a la ruta de MEIPASS

os.system('title ZPaqTUI By Wira - Ver. 60.6')

def get_zpaq_executable():
    """Devuelve la ruta de zpaq.exe, ya sea en el directorio actual o en MEIPASS si se ejecuta como .exe."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'zpaq.exe')  # Usar zpaq.exe extraído
    else:
        return 'zpaq.exe'  # Usar zpaq.exe en el directorio actual

def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla

        print("============================")
        print("     Archivos y Carpetas    ")
        print("============================")
        print("")

        # Listar archivos y carpetas en el directorio actual
        items = os.listdir('.')
        for index, item in enumerate(items):
            print(f"{index + 1}. {item}")

        print("")
        print("============================================================================")  # Línea de separación

        # Crear barra de opciones
        options = "[C]omprimir | [D]escomprimir | [E]liminar Archivo | [S]alir"
        print(f"{options:^{len('============================')}}")  # Centrar la barra
        print("============================================================================")  # Otra línea de separación

        print("Presiona C, D, E o S para seleccionar una opción.")

        option = msvcrt.getch().decode('utf-8').lower()  # Convertir a minúscula
        
        if option == 'c':
            compress(items)  # Pasar la lista de items
        elif option == 'd':
            decompress(items)  # Pasar la lista de items
        elif option == 'e':
            delete_file(items)  # Pasar la lista de items
        elif option == 's':
            break
        else:
            print("Opción inválida, intenta de nuevo.")
            input("Presiona Enter para continuar...")  # Esperar entrada del usuario

def compress(items):
    # Filtrar los elementos que no sean .zpaq
    valid_items = [item for item in items if not item.endswith(".zpaq")]

    if not valid_items:
        print("No se encontraron archivos ni carpetas para comprimir.")
        input("Presiona Enter para regresar al menú...")
        return

    choice = input("Escribe el número del archivo o carpeta a comprimir (o presiona Enter para cancelar): ")

    # Verificar si el usuario presionó Enter
    if choice == '':
        print("Acción cancelada.")
        input("Presiona Enter para regresar al menú...")
        return

    if choice.isdigit():
        choice = int(choice) - 1
        if 0 <= choice < len(valid_items):
            selected_item = valid_items[choice]
            print(f"Comprimiendo {selected_item}...")
            zpaq_executable = get_zpaq_executable()  # Obtener la ruta de zpaq.exe
            result = subprocess.run([zpaq_executable, "a", f"{selected_item}.zpaq", selected_item, "-m4", "-ssd"])
            if result.returncode == 0:
                print("Compresión completa.")
            else:
                print("Error en la compresión.")
        else:
            print("Opción inválida.")
    else:
        print("Entrada no válida.")
    
    input("Presiona Enter para regresar al menú...")

def decompress(items):
    # Filtrar solo los archivos .zpaq
    zpaq_files = [f for f in items if f.endswith(".zpaq")]
    
    # Comprobar si hay archivos .zpaq disponibles
    if not zpaq_files:
        print("No se encontraron archivos .zpaq para descomprimir.")
        input("Presiona Enter para regresar al menú...")
        return

    # Mostrar los archivos .zpaq listados
    print("Listado de archivos .zpaq disponibles para descomprimir:")
    for i, zpaq_file in enumerate(zpaq_files):
        print(f"{i + 1}. {zpaq_file}")

    # Solicitar al usuario que ingrese el número del archivo a descomprimir
    choice = input("Escribe el número del archivo a descomprimir (o presiona Enter para cancelar): ")

    # Verificar si el usuario presionó Enter
    if choice == '':
        print("Acción cancelada.")
        input("Presiona Enter para regresar al menú...")
        return

    # Validar la entrada del usuario
    if choice.isdigit():
        choice = int(choice) - 1  # Convertir a índice basado en cero
        if 0 <= choice < len(zpaq_files):
            selected_file = zpaq_files[choice]
            print(f"Descomprimiendo {selected_file}...")
            zpaq_executable = get_zpaq_executable()  # Obtener la ruta de zpaq.exe
            # Ejecutar el comando de descompresión
            result = subprocess.run([zpaq_executable, "x", selected_file])
            if result.returncode == 0:
                print("Descompresión completa.")
            else:
                print("Error en la descompresión.")
        else:
            print("Opción inválida.")  # Mensaje si el índice está fuera del rango
    else:
        print("Entrada no válida.")  # Mensaje si la entrada no es un número
    
    input("Presiona Enter para regresar al menú...")


def delete_file(items):
    if not items:
        print("No se encontraron archivos ni carpetas para eliminar.")
        input("Presiona Enter para regresar al menú...")
        return
    
    choice = input("Escribe el número del archivo o carpeta a eliminar (o presiona Enter para cancelar): ")

    if choice == '':
        print("Acción cancelada.")
        input("Presiona Enter para regresar al menú...")
        return

    if choice.isdigit():
        choice = int(choice) - 1
        if 0 <= choice < len(items):
            selected_item = items[choice]
            print(f"Eliminando {selected_item}...")
            try:
                if os.path.isdir(selected_item):
                    shutil.rmtree(selected_item)  # Eliminar carpeta y su contenido
                else:
                    os.remove(selected_item)  # Eliminar archivo
                print("Elemento eliminado.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
        else:
            print("Opción inválida.")
    else:
        print("Entrada no válida.")

    input("Presiona Enter para regresar al menú...")

if __name__ == "__main__":
    menu()
