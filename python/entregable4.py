# ==========================================
# SISTEMA DIPLOMADOSONLINE (SGA-DO)
# ==========================================

# --- 1. CLASES Y POO (Herencia y Polimorfismo) ---
class Persona:
    def __init__(self, cedula, nombre, correo):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo

class Alumno(Persona):
    def __init__(self, cedula, nombre, correo, tipo_programa):
        super().__init__(cedula, nombre, correo)
        self.tipo_programa = tipo_programa
        self.notas = [0, 0, 0]  # Inicializar en cero

    def evaluar_aprobacion(self):
        if len(self.notas) == 0 or all(n == 0 for n in self.notas):
            return False
        promedio = sum(self.notas) / len(self.notas)
        
        prog = self.tipo_programa.strip().lower()
        if "curso" in prog:
            return promedio >= 10
        elif "diplomado" in prog:
            return promedio >= 12
        elif "bootcamp" in prog:
            return promedio >= 14
        else:
            return promedio >= 10

class Profesor(Persona):
    def __init__(self, cedula, nombre, correo, especialidad, materia):
        super().__init__(cedula, nombre, correo)
        self.especialidad = especialidad
        self.materia = materia


# --- 2. ESTRUCTURAS DE DATOS (Pila para Deshacer) ---
pila_historial_notas = []  # LIFO


# --- 3. FUNCIONES DE PERSISTENCIA (Archivos .txt) ---
def guardar_alumno_en_txt(alumno):
    with open("alumnos.txt", "a", encoding="utf-8") as archivo:
        linea = f"{alumno.cedula}, {alumno.nombre}, {alumno.correo}, {alumno.tipo_programa}, {alumno.notas[0]}, {alumno.notas[1]}, {alumno.notas[2]}\n"
        archivo.write(linea)

def guardar_profesor_en_txt(profesor):
    with open("profesores.txt", "a", encoding="utf-8") as archivo:
        linea = f"{profesor.cedula}, {profesor.nombre}, {profesor.correo}, {profesor.especialidad}, {profesor.materia}\n"
        archivo.write(linea)


# --- 4. MENÚ PRINCIPAL Y LÓGICA ---
def mostrar_menu():
    print("\n=================================")
    print("SGA-DO: SISTEMA DIPLOMADOSONLINE")
    print("=================================")
    print("1. Registrar Alumno")
    print("2. Registrar Profesor")
    print("3. Registrar Notas a un Alumno")
    print("4. Deshacer Último Registro de Nota")
    print("5. Generar Cola de Certificados")
    print("6. Mostrar Reporte General")
    print("7. Salir")

def main():
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("Seleccione una opción (1-7): "))
            
            if opcion == 1:
                print("\n--- REGISTRO DE NUEVO ALUMNO ---")
                cedula = input("Ingrese Cédula (Ej. V-111): ")
                nombre = input("Ingrese Nombre Completo: ")
                correo = input("Ingrese Correo Electrónico: ")
                tipo_programa = input("Ingrese el Tipo de Programa (Curso, Diplomado, Bootcamp): ").capitalize()
                
                nuevo_alumno = Alumno(cedula, nombre, correo, tipo_programa)
                guardar_alumno_en_txt(nuevo_alumno)
                print(f"\n¡Éxito! Alumno {nombre} registrado y guardado en alumnos.txt.")

            elif opcion == 2:
                print("\n--- REGISTRO DE NUEVO PROFESOR ---")
                cedula = input("Ingrese Cédula (Ej. P-999): ")
                nombre = input("Ingrese Nombre Completo: ")
                correo = input("Ingrese Correo Electrónico: ")
                especialidad = input("Ingrese Especialidad (Ej. Backend): ")
                materia = input("Ingrese Materia Asignada (Ej. C++ y Algoritmos): ")
                
                nuevo_profesor = Profesor(cedula, nombre, correo, especialidad, materia)
                guardar_profesor_en_txt(nuevo_profesor)
                print(f"\n¡Éxito! Profesor {nombre} registrado y guardado en profesores.txt.")

            elif opcion == 3:
                print("\n--- REGISTRAR NOTA A UN ALUMNO ---")
                cedula_buscar = input("Ingrese la Cédula del alumno a buscar: ")
                alumnos_actualizados = []
                encontrado = False
                
                try:
                    with open("alumnos.txt", "r", encoding="utf-8") as archivo:
                        lineas = archivo.readlines()
                        
                    for linea in lineas:
                        datos = linea.strip().split(", ")
                        if len(datos) >= 7:
                            cedula = datos[0]
                            nombre = datos[1]
                            correo = datos[2]
                            tipo_prog = datos[3]
                            n1, n2, n3 = int(datos[4]), int(datos[5]), int(datos[6])
                            
                            if cedula == cedula_buscar:
                                encontrado = True
                                print(f"Alumno encontrado: {nombre} | Notas actuales: [{n1}, {n2}, {n3}]")
                                
                                if n1 != 0 and n2 != 0 and n3 != 0:
                                    print("[Aviso] Este alumno ya tiene sus 3 notas registradas.")
                                    alumnos_actualizados.append(linea)
                                else:
                                    nueva_nota = int(input("Ingrese la nota a registrar (0-20): "))
                                    
                                    if n1 == 0:
                                        n1 = nueva_nota
                                        idx_modificado = 0
                                    elif n2 == 0:
                                        n2 = nueva_nota
                                        idx_modificado = 1
                                    elif n3 == 0:
                                        n3 = nueva_nota
                                        idx_modificado = 2
                                        
                                    pila_historial_notas.append((cedula_buscar, idx_modificado))
                                    
                                    nueva_linea = f"{cedula}, {nombre}, {correo}, {tipo_prog}, {n1}, {n2}, {n3}\n"
                                    alumnos_actualizados.append(nueva_linea)
                                    print(f"¡Nota {nueva_nota} registrada con éxito!")
                            else:
                                alumnos_actualizados.append(linea)
                        else:
                            alumnos_actualizados.append(linea)
                            
                    with open("alumnos.txt", "w", encoding="utf-8") as archivo:
                        archivo.writelines(alumnos_actualizados)
                        
                    if not encontrado:
                        print(f"\n[Error] No se encontró ningún alumno con la cédula {cedula_buscar}.")
                        
                except FileNotFoundError:
                    print("\n[Error] El archivo alumnos.txt no existe todavía. Registre un alumno primero.")

            elif opcion == 4:
                print("\n--- DESHACER ÚLTIMO REGISTRO DE NOTA (PILAS) ---")
                if len(pila_historial_notas) == 0:
                    print("\n[Aviso] No hay acciones recientes en la pila para deshacer.")
                else:
                    cedula_afectada, idx_a_borrar = pila_historial_notas.pop()
                    
                    alumnos_actualizados = []
                    with open("alumnos.txt", "r", encoding="utf-8") as archivo:
                        lineas = archivo.readlines()
                        
                    for linea in lineas:
                        datos = linea.strip().split(", ")
                        if len(datos) >= 7:
                            cedula = datos[0]
                            nombre = datos[1]
                            correo = datos[2]
                            tipo_prog = datos[3]
                            n1, n2, n3 = int(datos[4]), int(datos[5]), int(datos[6])
                            
                            if cedula == cedula_afectada:
                                if idx_a_borrar == 0:
                                    n1 = 0
                                elif idx_a_borrar == 1:
                                    n2 = 0
                                elif idx_a_borrar == 2:
                                    n3 = 0
                                    
                            nueva_linea = f"{cedula}, {nombre}, {correo}, {tipo_prog}, {n1}, {n2}, {n3}\n"
                            alumnos_actualizados.append(nueva_linea)
                        else:
                            alumnos_actualizados.append(linea)
                            
                    with open("alumnos.txt", "w", encoding="utf-8") as archivo:
                        archivo.writelines(alumnos_actualizados)
                        
                    print(f"\n¡Se ha deshecho la última nota registrada para la cédula {cedula_afectada}!")

            elif opcion == 5:
                print("\n--- GENERAR COLA DE CERTIFICADOS (COLAS) ---")
                try:
                    from collections import deque
                    cola_certificados = deque()
                    
                    with open("alumnos.txt", "r", encoding="utf-8") as archivo:
                        lineas = archivo.readlines()
                        
                    for linea in lineas:
                        datos = linea.strip().split(", ")
                        if len(datos) >= 7:
                            cedula = datos[0]
                            nombre = datos[1]
                            correo = datos[2]
                            tipo_prog = datos[3]
                            
                            alum_temp = Alumno(cedula, nombre, correo, tipo_prog)
                            alum_temp.notas = [int(datos[4]), int(datos[5]), int(datos[6])]
                            
                            if alum_temp.evaluar_aprobacion():
                                cola_certificados.append(alum_temp)
                                
                    with open("certificados_pendientes.txt", "w", encoding="utf-8") as cert_file:
                        cert_file.write("=== LISTA DE GRADUANDOS / CERTIFICADOS PENDIENTES ===\n")
                        contador = 1
                        while len(cola_certificados) > 0:
                            graduando = cola_certificados.popleft()
                            promedio = sum(graduando.notas) / 3
                            linea_cert = f"{contador}. Cédula: {graduando.cedula} | Nombre: {graduando.nombre} | Programa: {graduando.tipo_programa} | Promedio: {promedio:.1f}\n"
                            cert_file.write(linea_cert)
                            contador += 1
                            
                    print(f"\n¡Cola procesada con éxito! Se generó el archivo 'certificados_pendientes.txt'.")
                    
                except FileNotFoundError:
                    print("\n[Error] El archivo alumnos.txt no existe.")

            elif opcion == 6:
                print("\n=================================")
                print("       REPORTE GENERAL DEL SGA     ")
                print("=================================")
                
                print("\n--- LISTADO DE ALUMNOS ---")
                try:
                    with open("alumnos.txt", "r", encoding="utf-8") as archivo:
                        for linea in archivo:
                            datos = linea.strip().split(", ")
                            if len(datos) >= 7:
                                print(f"Cédula: {datos[0]} | Nombre: {datos[1]} | Correo: {datos[2]} | Programa: {datos[3]} | Notas: [{datos[4]}, {datos[5]}, {datos[6]}]")
                except FileNotFoundError:
                    print("No hay registros de alumnos todavía.")
                    
                print("\n--- LISTADO DE PROFESORES ---")
                try:
                    with open("profesores.txt", "r", encoding="utf-8") as archivo:
                        for linea in archivo:
                            datos = linea.strip().split(", ")
                            if len(datos) >= 5:
                                print(f"Cédula: {datos[0]} | Nombre: {datos[1]} | Correo: {datos[2]} | Especialidad: {datos[3]} | Materia: {datos[4]}")
                except FileNotFoundError:
                    print("No hay registros de profesores todavía.")
                print("=================================")

            elif opcion == 7:
                print("\nSaliendo del sistema...")
                break
            else:
                print("\n[Advertencia] Opción fuera de rango (1-7).")
                
        except ValueError:
            print("\n[Error]: Ingrese un valor numérico válido.")

if __name__ == "__main__":
    main()