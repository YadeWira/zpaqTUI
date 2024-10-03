import os
import subprocess
import msvcrt
import shutil  # Importar shutil para eliminar directorios no vacíos
import sys  # Importar sys para acceder a la ruta de MEIPASS

os.system('title ZPaqTUI By Wira - Ver. 60.6 - TUI a0.1')

def get_zpaq_executable():
    """Devuelve la ruta de zpaq.exe, ya sea en el directorio actual o en MEIPASS si se ejecuta como .exe."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'zpaq.exe')  # Usar zpaq.exe extraído
    else:
        return 'zpaq.exe'  # Usar zpaq.exe en el directorio actual

def print_menu(items, selected_index, page, items_per_page):
    """Imprime el menú con paginación y el elemento seleccionado resaltado."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
    print("  =======================")
    print("  # Archivos y Carpetas #")
    print("  =======================")
    print("")

    start = page * items_per_page
    end = start + items_per_page
    visible_items = items[start:end]

    for index, item in enumerate(visible_items):
        if index == selected_index:
            print(f"> {item} <")  # Resaltar el elemento seleccionado
        else:
            print(f"  {item}")

    print("")
    print(f"  Página {page + 1} de {((len(items) - 1) // items_per_page) + 1}")
    print("============================================================================")
    options = "| [C]omprimir | [D]escomprimir | [E]liminar | [R]efrescar | [S]alir | [<] Anterior | [>] Siguiente |"
    print(f"{options:^{len('============================')}}")
    print("============================================================================")

def menu():
    items_per_page = 20  # Número de archivos a mostrar por página
    page = 0  # Página actual
    selected_index = 0  # Índice del elemento seleccionado en la página

    while True:
        # Recargar la lista de archivos antes de mostrar el menú
        items = os.listdir('.')
        
        # Asegurar que el índice seleccionado esté dentro del rango de la página actual
        max_page = (len(items) - 1) // items_per_page
        page = min(max_page, max(0, page))  # Limitar la página a un valor válido
        selected_index = selected_index % items_per_page

        print_menu(items, selected_index, page, items_per_page)
        key = msvcrt.getch()

        # Manejo de teclas de flecha
        if key == b'\xe0':  # Tecla de función (Flechas)
            key = msvcrt.getch()
            if key == b'H':  # Flecha arriba
                selected_index = (selected_index - 1) % items_per_page
            elif key == b'P':  # Flecha abajo
                selected_index = (selected_index + 1) % items_per_page
            elif key == b'K':  # Flecha izquierda (Página anterior)
                page = max(0, page - 1)
                selected_index = 0
            elif key == b'M':  # Flecha derecha (Página siguiente)
                page = min(max_page, page + 1)
                selected_index = 0
        elif key == b'\r':  # Enter
            selected_item = items[page * items_per_page + selected_index]
            action_menu(selected_item, items)
        elif key == b'c':  # Comprimir
            compress(items, selected_index, page, items_per_page)
        elif key == b'd':  # Descomprimir
            decompress(items, selected_index, page, items_per_page)
        elif key == b'e':  # Eliminar archivo
            delete_file(items, selected_index, page, items_per_page)
        elif key == b'r':  # Refrescar lista
            continue  # Simplemente recargar el menú
        elif key == b's':  # Salir
            break
        else:
            print("Opción inválida, intenta de nuevo.")
            input("Presiona Enter para continuar...")  # Esperar entrada del usuario

def action_menu(selected_item, items):
    """Muestra el submenú después de que el usuario selecciona un archivo."""
    print(f"Has seleccionado: {selected_item}")
    input("Presiona Enter para regresar al menú...")

def compress(items, selected_index, page, items_per_page):
    """Comprime el archivo seleccionado."""
    full_index = page * items_per_page + selected_index
    
    valid_items = [item for item in items if not item.endswith(".zpaq")]

    if not valid_items:
        print("No se encontraron archivos ni carpetas para comprimir.")
        input("Presiona Enter para regresar al menú...")
        return

    if full_index < len(valid_items):
        selected_item = valid_items[full_index]
    else:
        print("El índice seleccionado no es válido.")
        input("Presiona Enter para regresar al menú...")
        return

    print(f"Comprimiendo {selected_item}...")
    zpaq_executable = get_zpaq_executable()
    result = subprocess.run([zpaq_executable, "a", f"{selected_item}.zpaq", selected_item, "-m4", "-ssd"])
    if result.returncode == 0:
        print("Compresión completa.")
    else:
        print("Error en la compresión.")

    input("Presiona Enter para regresar al menú...")

def decompress(items, selected_index, page, items_per_page):
    """Descomprime el archivo .zpaq seleccionado."""
    full_index = page * items_per_page + selected_index
    
    zpaq_files = [f for f in items if f.endswith(".zpaq")]

    if not zpaq_files:
        print("No se encontraron archivos .zpaq para descomprimir.")
        input("Presiona Enter para regresar al menú...")
        return

    if full_index < len(zpaq_files):
        selected_file = zpaq_files[full_index]
    else:
        print("El índice seleccionado no es válido.")
        input("Presiona Enter para regresar al menú...")
        return

    print(f"Descomprimiendo {selected_file}...")
    zpaq_executable = get_zpaq_executable()
    result = subprocess.run([zpaq_executable, "x", selected_file])
    if result.returncode == 0:
        print("Descompresión completa.")
    else:
        print("Error en la descompresión.")

    input("Presiona Enter para regresar al menú...")

def delete_file(items, selected_index, page, items_per_page):
    """Elimina el archivo o carpeta seleccionada."""
    full_index = page * items_per_page + selected_index
    selected_item = items[full_index]
    
    confirmation = input(f"¿Estás seguro de que deseas eliminar {selected_item}? (S/N): ").lower()
    if confirmation == 's':
        print(f"Eliminando {selected_item}...")
        try:
            if os.path.isdir(selected_item):
                shutil.rmtree(selected_item)
            else:
                os.remove(selected_item)
            print("Elemento eliminado.")
        except Exception as e:
            print(f"Error al eliminar: {e}")
    else:
        print("Operación de eliminación cancelada.")
    
    input("Presiona Enter para regresar al menú...")

if __name__ == "__main__":
    menu()
