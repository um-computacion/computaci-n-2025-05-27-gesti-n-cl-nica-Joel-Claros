from datetime import datetime

class Paciente():
    def __init__(
        self, 
        el_nombre, 
        el_dni, 
        la_fecha
    ):  
        if not el_nombre or not el_dni or not la_fecha:
            raise ValueError("Es obligatorio ingresar todos los campos")
        self.dni = el_dni  
        self.nombre = el_nombre 
        self.fecha_nacimiento = la_fecha 

    def obtener_dni(self) -> str:
        return self.dni
        
    def __str__(self) -> str:
        return f'Paciente(DNI: {self.dni}, Nombre: {self.nombre}, Fecha Nac: {self.fecha_nacimiento})'

class Especialidad():
    def __init__(
        self, 
        el_tipo: str, 
        los_dias: list[str]
    ):  
        if not el_tipo or not los_dias:
            raise ValueError("Es obligatorio ingresar todos los campos")
        self.tipo = el_tipo
        self.dias = [dia.lower() for dia in los_dias] 

    def obtener_especialidad(self) -> str:
        return self.tipo
    
    def verificar_dia(self, dia: str):
        return dia.lower() in self.dias

    def __str__(self) -> str:
        dias_str = ", ".join(self.dias)
        return f'{self.tipo} (Días: {dias_str})'

class Medico():
    def __init__(
        self, 
        el_nombre_medico: str, 
        la_matricula: str,
        las_especialidades: list[Especialidad] = None
    ):  
        if not la_matricula or not el_nombre_medico:
            raise ValueError("Es obligatorio ingresar todos los campos")
        self.matricula = la_matricula 
        self.nombre = el_nombre_medico 
        self.especialidades = {} 
        
        if las_especialidades:
            for esp in las_especialidades:
                self.agregar_especialidad(esp) 

    def agregar_especialidad(self, especialidad: Especialidad):
        if not isinstance(especialidad, Especialidad):
            raise ValueError("La especialidad debe ser una instancia de la clase Especialidad.")
        self.especialidades[especialidad.obtener_especialidad().lower()] = especialidad

    def obtener_matricula(self) -> str:
        return self.matricula
    
    def obtener_nombre(self) -> str: 
        return self.nombre
    
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for j in self.especialidades.values():
            if j.verificar_dia(dia):
                return j.obtener_especialidad()
        return None

    def __str__(self) -> str:
        especialidades_str = ", ".join([self.obtener_especialidad_para_dia() for e in self.especialidades.values()]) # CAMBIADO
        return f'Medico(Matrícula: {self.matricula}, Nombre: {self.nombre}, Especialidades: [{especialidades_str}])'
    
class Turno():
    def __init__(
        self,
        el_paciente: Paciente, 
        el_medico: Medico, 
        la_fecha_hora: datetime,
        la_especialidad: str
    ):
        if not el_paciente or not el_medico or not la_fecha_hora or not la_especialidad:
            raise ValueError("Es obligatorio ingresar todos los campos")

        self.paciente = el_paciente 
        self.medico = el_medico       
        self.fecha_hora = la_fecha_hora
        self.especialidad = la_especialidad 

    def obtener_medico(self) -> Medico:
        return self.medico
    
    def obtener_fecha_hora(self) -> datetime:
        return self.fecha_hora

    def __str__(self) -> str:
        return f"Paciente: {self.paciente.nombre}, Medico: {self.medico.nombre}, Fecha_Hora: {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}, Especialidad: {self.especialidad}"


class Receta():
    def __init__(
        self, 
        el_paciente: Paciente, 
        el_medico: Medico, 
        los_medicamentos: list[str], 
    ): 
        if not el_paciente or not el_medico: 
            raise ValueError("Paciente y Médico son obligatorios para la receta.")
        if not los_medicamentos:
            raise ValueError("La lista de medicamentos no puede estar vacía.")

        self.paciente = el_paciente
        self.medico = el_medico     
        self.medicamentos = list(los_medicamentos) 
        self.fecha_receta = datetime.now()

    def __str__(self) -> str:
        return (f'Receta (Paciente: {self.paciente.nombre} (DNI: {self.paciente.dni}), '
                f'Médico: {self.medico.nombre} (Matrícula: {self.medico.matricula}), '
                f'Medicamentos: {", ".join(self.medicamentos)}, '
                f'Fecha: {self.fecha_receta.strftime("%d/%m/%Y")})')
    

class Historia_Clinica():
    def __init__(
        self,
        el_paciente: Paciente
    ):
        self.paciente = el_paciente 
        self.turnos = []
        self.recetas = []

    def agregar_receta(self, receta: Receta): 
        self.recetas.append(receta)
        
    def agregar_turno(self, turno: Turno): 
        self.turnos.append(turno)
    
    def obtener_turnos(self) -> list[Turno]:
        return list(self.turnos)

    def obtener_recetas(self) -> list[Receta]:
        return list(self.recetas) 

    def __str__(self) -> str:
        return (f'Historia Clínica de {self.paciente.nombre} (DNI: {self.paciente.dni})'
                f'   Total de Turnos: {len(self.turnos)}'
                f'   Total de Recetas: {len(self.recetas)}')
    

class PacienteNoExisteError(Exception): pass
class MedicoNoExisteError(Exception): pass
class TurnoDuplicadoError(Exception): pass
class RecetaInvalidaException(Exception): pass
class TurnoPasadoError(Exception): pass
class Clinica():
    def __init__(
        self
    ):  
        self.pacientes = {}
        self.medicos = {} 
        self.turnos = [] 
        self.historias_clinicas = {} 

    def agregar_paciente(self, paciente: Paciente) -> bool:
        if paciente.obtener_dni() in self.pacientes:
            raise ValueError("Este paciente ya ha sido registrado") 
        self.pacientes[paciente.obtener_dni()] = paciente 
        self.historias_clinicas[paciente.obtener_dni()] = Historia_Clinica(paciente) 
       
    
    def agregar_medico(self, medico: Medico) -> bool:
        if medico.obtener_matricula() in self.medicos:
            raise ValueError("Este médico ya ha sido registrado") 
        self.medicos[medico.obtener_matricula()] = medico 
        
        
    def obtener_pacientes(self) -> list[Paciente]:
        return list(self.pacientes.values())
    
    def obtener_medicos(self) -> list[Medico]: 
        return list(self.medicos.values())
    
    def obtener_medico_por_matricula(self, matricula: str) -> Medico:
        medico = self.medicos.get(matricula)
        if not medico:
            raise MedicoNoExisteError(matricula)
        return medico

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime) -> Turno:
        self.validar_existencia_paciente(dni) 
        paciente_obj = self.pacientes[dni] 
        self.validar_existencia_medico(matricula)
        medico_obj = self.medicos[matricula] 
        
        if fecha_hora < datetime.now():
            raise TurnoPasadoError(fecha_hora)
        
        dia_semana_turno = self.obtener_dia_semana_en_espanol(fecha_hora)
        
        especialidad_valida_para_dia = False
        for esp_obj in medico_obj.especialidades.values():
            if esp_obj.obtener_especialidad().lower() == especialidad.lower() and esp_obj.verificar_dia(dia_semana_turno):
                especialidad_valida_para_dia = True
                break
        
        if not especialidad_valida_para_dia:
            raise MedicoNoExisteError(f"El médico con matrícula '{matricula}' no atiende la especialidad '{especialidad}' el día '{dia_semana_turno}'.") 

        self.validar_turno_no_duplicado(matricula, fecha_hora)
        
        nuevo_turno = Turno(paciente_obj, medico_obj, fecha_hora, especialidad)
        
        self.turnos.append(nuevo_turno)
        self.historias_clinicas[dni].agregar_turno(nuevo_turno) 
        
        return nuevo_turno

    def obtener_turnos(self) -> list[Turno]: 
        return list(self.turnos)
                    
    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        if dni not in self.pacientes: 
            raise RecetaInvalidaException("Paciente no encontrado.") 
        if matricula not in self.medicos:
            raise RecetaInvalidaException("Médico no encontrado.") 
        nueva_receta = Receta(self.pacientes[dni], self.medicos[matricula], medicamentos)
        self.historias_clinicas[dni].agregar_receta(nueva_receta) 


    def obtener_historia_clinica(self, dni: str) -> Historia_Clinica: 
        historia = self.historias_clinicas.get(dni)
        if not historia:
            raise PacienteNoExisteError(dni) 
        return historia

    def validar_existencia_paciente(self, dni: str):
        if dni not in self.pacientes:
            raise PacienteNoExisteError(dni) 
            
    def obtener_todos_los_turnos(self) -> list[Turno]: 
        return list(self.turnos) 
    
    def validar_existencia_medico(self, matricula: str):
        if matricula not in self.medicos:
            raise MedicoNoExisteError(matricula) 

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        medico_obj = self.medicos[matricula]
        for turno in self.turnos:
            if (turno.obtener_medico().obtener_matricula() == matricula and 
                turno.obtener_fecha_hora() == fecha_hora):
                raise TurnoDuplicadoError(medico_obj.nombre, fecha_hora) 
                                                                        

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias_semana = {0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",4: "viernes", 5: "sábado", 6: "domingo"}
        return dias_semana[fecha_hora.weekday()]

    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:
        dia_semana_lower = dia_semana.lower()
        if dia_semana_lower not in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]:
            raise ValueError()
        especialidad_encontrada = medico.obtener_especialidad_para_dia(dia_semana_lower)
        if especialidad_encontrada:
            return especialidad_encontrada
        else:
            raise ValueError("Especialidad no encontrada") 

    def validar_especialidad_en_dia(self, medico: Medico,especialidad_solicitada: str, dia_semana: str):
        pass


    def __str__(self) -> str:
        return (f"Clínica (Pacientes: {len(self.pacientes)}, Médicos: {len(self.medicos)}, "
                f"Turnos: {len(self.turnos)})")