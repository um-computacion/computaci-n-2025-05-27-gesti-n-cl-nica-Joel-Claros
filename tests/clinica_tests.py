import unittest

from datetime import datetime, timedelta

from modelo.clinica import *

class TestClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Juan Gabriel", "3265524", "01/01/1990")
        self.medico = Medico("Fabricio Romano", "M734")
        self.especialidad = Especialidad("Clínica", ["lunes"])
        self.medico.agregar_especialidad(self.especialidad)
        

        hoy = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)

        dias_hasta_lunes = (0 - hoy.weekday() + 7) % 7 
        if dias_hasta_lunes == 0: 
            dias_hasta_lunes = 7
        self.fecha = hoy + timedelta(days=dias_hasta_lunes)


        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

    def test_paciente_duplicado(self):
        with self.assertRaises(ValueError):
            self.clinica.agregar_paciente(self.paciente)

    def test_turno_de_forma_correcta(self):
        turno_agendado = self.clinica.agendar_turno("3265524", "M734", "Clínica", self.fecha)
        self.assertEqual(len(self.clinica.obtener_turnos()), 1)

        self.assertEqual(turno_agendado.paciente.obtener_dni(), "3265524")
        self.assertEqual(turno_agendado.medico.obtener_matricula(), "M734")
        self.assertEqual(turno_agendado.especialidad, "Clínica")
        self.assertEqual(turno_agendado.obtener_fecha_hora(), self.fecha)


    def test_paciente_no_existe(self):
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.agendar_turno("999", "M734", "Clínica", self.fecha)

    def test_medico_no_existe(self):
        with self.assertRaises(MedicoNoExisteError):
            self.clinica.agendar_turno("3265524", "M567", "Clínica", self.fecha)

    def test_turno_duplicado(self):
        self.clinica.agendar_turno("3265524", "M734", "Clínica", self.fecha)
        with self.assertRaises(TurnoDuplicadoError):
            self.clinica.agendar_turno("3265524", "M734", "Clínica", self.fecha)
    
    def test_turno_pasado(self):
        fecha_pasada = datetime(2023, 1, 1, 10, 0) 
        with self.assertRaises(TurnoPasadoError):
            self.clinica.agendar_turno(self.paciente.obtener_dni(), self.medico.obtener_matricula(), "Clínica", fecha_pasada)

    def test_turno_dia_incorrecto(self):
        fecha_mal_dia = datetime(2025, 6, 17, 10, 0) 
        with self.assertRaises(TurnoPasadoError):
            self.clinica.agendar_turno("3265524", "M734", "Clínica", fecha_mal_dia)

    def test_receta_valida(self):
        self.clinica.emitir_receta("3265524", "M734", ["Redoxon"])
        historia = self.clinica.obtener_historia_clinica("3265524")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_receta_medicamento_vacio(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, self.medico, [])

    def test_receta_paciente_no_existe(self):
        with self.assertRaises(RecetaInvalidaException): 
            self.clinica.emitir_receta("567", "M734", ["Redoxon"])

    def test_receta_medico_no_existe(self):
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("3265524", "M567", ["Redoxon"])

    def test_historia_clinica_paciente_no_exite(self):
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.obtener_historia_clinica("567")

if __name__ == "__main__":
    unittest.main()