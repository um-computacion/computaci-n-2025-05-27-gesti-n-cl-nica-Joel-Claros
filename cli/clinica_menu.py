from datetime import datetime
from modelo.clinica import (Clinica, Paciente, Medico, Turno, Receta, Historia_Clinica, Especialidad,  PacienteNoExisteError, MedicoNoExisteError, RecetaInvalidaException, TurnoDuplicadoError, TurnoPasadoError)
class CLI:
    def __init__(self):
        self.clinica = Clinica()


    def mostrar_menu(self):
        print("---Menu Clínica---")
        print ("1) Agregar paciente")
        print ("2) Agregar médico")
        print ("3) Agregar turno") 
        print ("4) Emitir Receta")
        print ("5) Ver Historia Clínica") 
        print ("6) Ver todos los turnos")
        print ("7) Ver todos los pacientes")
        print ("8) Ver todos los médicos")
        print ("9) Salir")
        
    def ejecutar(self):
        while True:
            self.mostrar_menu()
            respuesta = input("Seleccione el número de la acción que desea realizar: ").strip()
            
            if respuesta == "1":
                self.agregar_paciente()
            elif respuesta == "2":
                self.agregar_medico()
            elif respuesta == "3":
                self.agendar_turno()
            elif respuesta == "4":
                self.agregar_especialidad_a_medico_existente()
            elif respuesta == "5":
                self.emitir_receta()
            elif respuesta == "6":
                self.ver_historia_clinica()
            elif respuesta == "7":
                self.ver_todos_los_turnos()
            elif respuesta == "8":
                self.ver_todos_los_pacientes()
            elif respuesta == "9":
                self.ver_todos_los_medicos()
            elif respuesta == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
            
            input("Presione Enter para continuar")


    def agregar_paciente(self):
        print("--- Agregar Paciente ---")
        dni = input("Ingrese DNI del paciente: ")
        nombre = input("Ingrese nombre del paciente: ")
        fecha_nac = input("Ingrese fecha de nacimiento (dd/mm/aaaa): ")
        paciente = Paciente(dni, nombre, fecha_nac)
        self.clinica.agregar_paciente(paciente)
        print(f"Paciente '{nombre}' ({dni}) agregado con éxito")


    def agregar_medico(self):
        print("--- Agregar Médico ---")
        matricula = input("Ingrese matrícula del médico: ")
        nombre = input("Ingrese nombre completo del médico: ")
        especialidad = input("Ingrese especialidad del médico: ")
        medico = Medico(matricula, nombre, especialidad)
        self.clinica.agregar_medico(medico) 
    
    def agregar_especialidad_a_medico_existente(self, matricula: str = None):
        print("--- Agregar Especialidad a Médico ---")
        matricula = input("Matrícula del médico: ")
        tipo = input("Nombre de la especialidad: ")
        dias = input("Días de atención (separados por coma): ").split(',')
        medico = self.clinica.obtener_medico_por_matricula(matricula)
        medico.agregar_especialidad(Especialidad(tipo, dias))
        print("Especialidad agregada.")


    def agendar_turno(self):
        print("--- Agendar Turno ---")
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        fecha_str = input("Fecha del turno (dd/mm/aaaa): ")
        hora_str = input("Hora del turno (hh:mm): ")
        fecha_hora_str = f"{fecha_str} {hora_str}"
        fecha_hora = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
        self.clinica.agendar_turno(dni, matricula, fecha_hora)
   

    def emitir_receta(self):
        print("--- Emitir Receta ---")
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        medicamentos_str = input("Medicamentos (separados por coma): ")
        
        medicamentos = [m.strip() for m in medicamentos_str.split(',') if m.strip()] 
        self.clinica.emitir_receta(dni, matricula, medicamentos) 

    def ver_historia_clinica(self):
        print("--- Ver Historia Clínica ---")
        dni = input("DNI del paciente: ")
        hola = self.clinica.obtener_historia_clinica(dni) 
        print(hola)

    def ver_todos_los_turnos(self):
        print("--- Todos los Turnos Agendados ---")
        turnos = self.clinica.obtener_todos_los_turnos()
        if not turnos:
            print("No hay turnos agendados.")

    def ver_todos_los_pacientes(self):
        print("--- Todos los Pacientes Registrados ---")
        pacientes = self.clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")

    def ver_todos_los_medicos(self):
        print("--- Todos los Médicos Registrados ---")
        medicos = self.clinica.obtener_medicos()
        if not medicos:
            print("No hay médicos registrados.")



if __name__ == "__main__":
    cli_app = CLI()
    cli_app.ejecutar()