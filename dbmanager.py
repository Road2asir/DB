import sqlite3
import os

class dbconnector:
    pass

class sqlconnector(dbconnector):
    def __init__(self):
        self._connection=sqlite3.connect(''.join([os.getcwd(),f'/db/CP_UD5.db']))
        self.cursor=self._connection.cursor()

    def create_table(self, table_name, *attribute):
        attribute = ','.join(attribute)
        command = f"""CREATE TABLE IF NOT EXISTS {table_name} ({attribute});
        """
        self.cursor.execute(command)
        self._connection.commit()

    def drop_table(self, table_name):
        command = f'DROP TABLE {table_name}'
        self.cursor.execute(command)
        
        return f'{table_name} dropped'

    def obtener_empleados(self, n_hijos=None):
        if n_hijos is not None:
            empleados = self._filtrar_hijos(n_hijos)

        else:
            obj = self.cursor.execute("""
            SELECT *
            FROM Empleados
                                      """)
            empleados = obj.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        return empleados, column_names

    def insertar_empleado(self, dni, nombre, apellidos, fecha_nac, n_hijos, estatura):
        """
          Registra nuevo empleado en la db

    """
        self.cursor.execute("""
                            INSERT INTO Empleados
                            (DNI, Nombre, Apellidos, Fecha_Nacimiento,
                            N_hijos, estatura)
                            VALUES (?,?,?,?,?,?); 
                            """,
                            (dni, nombre, apellidos, fecha_nac, 
                             n_hijos, estatura)
                            )
        self._connection.commit()

    def _filtrar_hijos(self, n_hijos):
        """
        Obtener los datos de los empleados que tengan uno,
        dos, tres o cinco hijos.
        """
        if n_hijos is not None:
            obj = self.cursor.execute("""
            SELECT * FROM Empleados WHERE N_hijos IN (?)
                                      """,
                                      (n_hijos,))
            return obj.fetchall()
        else:
            return False


    def _filtrar_fecha(self):
        """
        Obtener los datos de empleados que nacieron entre el 
        01/01/1985 y el 31/12/2000
        """
        fecha1 = '1985-01-01'
        fecha2 = '2000-12-31'
        obj=self.cursor.execute("""
        SELECT * FROM Empleados WHERE Fecha_Nacimiento BETWEEN ? AND ?
        """, (fecha1, fecha2,))
        column_names = [description[0] for description in self.cursor.description]
        return obj.fetchall(), column_names

    def obtener_nulls(self):
        """
        Obtener los datos de los empleados que no han introducido
        el número de hijos en la casilla correspondiente.
        """
        obj=self.cursor.execute("""
            SELECT * 
            FROM Empleados
            WHERE N_hijos IS NULL;
                                """)
        column_names = [description[0] for description in self.cursor.description]
        return obj.fetchall(), column_names

    def nueva_columna(self):
        """
        Crea una nueva columna en la tabla Empleados, 
        llamada “nombreApellidos” cuyo contenido será
        el nombre y los apellidos concatenados, 
        separados por un espacio en blanco.
        """
        self.cursor.execute(f"""
        ALTER TABLE Empleados
        ADD COLUMN nombreApellidos TEXT
        """)
        self.cursor.execute("""
        UPDATE Empleados
        SET nombreApellidos = Nombre || ' ' || Apellidos
        """)
        self._connection.commit()

    def punto2_1(self):
        obj = self.cursor.execute("""
            SELECT *
            FROM Empleados
            WHERE N_hijos IN (?,?,?,?)
            """,
                            (1,2,3,5))
        empleados = obj.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        return empleados, column_names

    def punto2_2(self):
        return self._filtrar_fecha()

    def reset(self):
        tables=['Empleados',]
        for table in tables:
            self.cursor.execute(f"""DELETE FROM {table}
        """)
            self._connection.commit()

    def close(self):
        self._connection.close()

