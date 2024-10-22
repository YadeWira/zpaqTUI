import os
import subprocess
import msvcrt
import shutil  # Importar shutil para eliminar directorios no vacíos
import sys  # Importar sys para acceder a la ruta de MEIPASS

os.system('title ZPaqTUI By Wira - zpaqfranz Ver. 60.8o - TUI a0.3 - x86')

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
    print("====================================================================================================")
    options = "| [C]omprimir | [D]escomprimir | [E]liminar | [R]efrescar | [S]alir | [<] Anterior | [>] Siguiente |"
    print(f"{options:^{len('============================')}}")
    print("====================================================================================================")

def get_absolute_index(page, selected_index, items_per_page):
    """Obtiene el índice absoluto de un elemento basado en la página y la selección."""
    return page * items_per_page + selected_index

def menu():
    items_per_page = 20  # Número de archivos a mostrar por página
    page = 0  # Página actual
    selected_index = 0  # Índice del elemento seleccionado en la página

    while True:
        try:
            # Recargar la lista de archivos antes de mostrar el menú
            items = os.listdir('.')

            # Separar carpetas y archivos, ordenando para que carpetas vayan primero
            folders = [item for item in items if os.path.isdir(item)]
            files = [item for item in items if os.path.isfile(item)]
            items = folders + files  # Carpetas primero, luego archivos
            
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
                # Verificar si el índice seleccionado es válido antes de proceder
                absolute_index = get_absolute_index(page, selected_index, items_per_page)
                if 0 <= absolute_index < len(items):
                    selected_item = items[absolute_index]
                    action_menu(selected_item, items)
                else:
                    print("El índice seleccionado no es válido.")
                    input("Presiona Enter para regresar al menú...")
            elif key == b'c':  # Comprimir
                compress(items, selected_index, page, items_per_page)
            elif key == b'd':  # Descomprimir
                decompress(items, selected_index, page, items_per_page)
            elif key == b'e':  # Eliminar archivo
                delete_file(items, selected_index, page, items_per_page)  # Pasar page e items_per_page
            elif key == b'r':  # Refrescar lista
                continue  # Simplemente recargar el menú
            elif key == b's':  # Salir
                break
            else:
                print("Opción inválida, intenta de nuevo.")
                input("Presiona Enter para continuar...")  # Esperar entrada del usuario
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            input("Presiona Enter para continuar...")  # Esperar entrada del usuario

def action_menu(selected_item, items):
    """Muestra el submenú después de que el usuario selecciona un archivo."""
    print(f"Has seleccionado: {selected_item}")
    input("Presiona Enter para regresar al menú...")

def compress(items, selected_index, page, items_per_page):
    valid_items = [item for item in items if not item.endswith(".zpaq")]

    if not valid_items:
        print("No se encontraron archivos ni carpetas para comprimir.")
        input("Presiona Enter para regresar al menú...")
        return

    # Calcular el índice absoluto dentro de la lista completa
    absolute_index = get_absolute_index(page, selected_index, items_per_page)

    # Asegurar que el índice absoluto esté dentro del rango de archivos válidos
    if 0 <= absolute_index < len(valid_items):
        selected_item = valid_items[absolute_index]
        print(f"Comprimiendo {selected_item}...")
        zpaq_executable = get_zpaq_executable()

        try:
            result = subprocess.run([zpaq_executable, "a", f"{selected_item}.zpaq", selected_item, "-m4", "-ssd"])
            if result.returncode == 0:
                print("Compresión completa.")
            else:
                print("Error en la compresión.")
        except Exception as e:
            print(f"Ocurrió un error al intentar comprimir: {e}")
    else:
        print("El índice seleccionado no es válido.")

    input("Presiona Enter para regresar al menú...")

def decompress(items, selected_index, page, items_per_page):
    zpaq_files = [f for f in items if f.endswith(".zpaq")]

    if not zpaq_files:
        print("No se encontraron archivos .zpaq para descomprimir.")
        input("Presiona Enter para regresar al menú...")
        return

    # Calcular el índice absoluto dentro de la lista completa
    absolute_index = get_absolute_index(page, selected_index, items_per_page)

    # Asegurar que el índice absoluto esté dentro del rango de archivos .zpaq
    if 0 <= absolute_index < len(items) and items[absolute_index].endswith(".zpaq"):
        selected_file = items[absolute_index]
        print(f"Descomprimiendo {selected_file}...")
        zpaq_executable = get_zpaq_executable()

        try:
            result = subprocess.run([zpaq_executable, "x", selected_file])
            if result.returncode == 0:
                print("Descompresión completa.")
            else:
                print("Error en la descompresión.")
        except Exception as e:
            print(f"Ocurrió un error al intentar descomprimir: {e}")
    else:
        print("El índice seleccionado no es válido para descomprimir.")

    input("Presiona Enter para regresar al menú...")

def delete_file(items, selected_index, page, items_per_page):
    try:
        # Calcular el índice absoluto dentro de la lista completa
        absolute_index = get_absolute_index(page, selected_index, items_per_page)

        # Asegurarse de que el índice absoluto esté dentro del rango
        if 0 <= absolute_index < len(items):
            selected_item = items[absolute_index]
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
        else:
            print("El índice seleccionado no es válido.")
        
        input("Presiona Enter para regresar al menú...")
    except IndexError:
        print("El índice seleccionado no es válido para eliminar.")
        input("Presiona Enter para regresar al menú...")

if __name__ == "__main__":
    menu()