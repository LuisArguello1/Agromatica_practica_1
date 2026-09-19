import os
import unittest
import warnings

import pandas as pd
import psycopg2

warnings.filterwarnings("ignore", category=UserWarning)  # aviso de pandas con psycopg2

DB_CONFIG = {
    "dbname": "agrobio_db",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432",
}


class BaseDB(unittest.TestCase):
    """Abre una conexión por grupo de pruebas y la cierra al terminar."""

    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg2.connect(**DB_CONFIG)
        cls.cur = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.cur.close()
        cls.conn.close()

    def uno(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()[0]

    def todos(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()


# 5.1 Pruebas de conexión
class TestConexion(BaseDB):
    def test_conexion_abierta(self):
        self.assertEqual(self.conn.closed, 0)

    def test_version_postgresql(self):
        self.assertIn("PostgreSQL", self.uno("SELECT version()"))

    def test_lectura_con_pandas(self):
        df = pd.read_sql("SELECT cultivo, rendimiento FROM cultivos", self.conn)
        self.assertFalse(df.empty)
        self.assertListEqual(list(df.columns), ["cultivo", "rendimiento"])


# 5.2 Validación de datos insertados (pruebas unitarias sobre las tablas)
class TestDatosInsertados(BaseDB):
    def columnas(self, tabla):
        self.cur.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = %s ORDER BY ordinal_position",
            (tabla,),
        )
        return [fila[0] for fila in self.cur.fetchall()]

    def test_tablas_existen(self):
        filas = self.todos(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public'"
        )
        self.assertTrue({"genes", "cultivos"} <= {f[0] for f in filas})

    def test_columnas_genes(self):
        self.assertListEqual(
            self.columnas("genes"), ["id", "especie", "nombre", "longitud"]
        )

    def test_columnas_cultivos(self):
        self.assertListEqual(
            self.columnas("cultivos"),
            ["id", "cultivo", "anio", "produccion", "rendimiento"],
        )

    def test_registros_genes(self):
        self.assertEqual(self.uno("SELECT COUNT(*) FROM genes"), 5)

    def test_registros_cultivos(self):
        self.assertEqual(self.uno("SELECT COUNT(*) FROM cultivos"), 15)

    def test_sin_valores_nulos(self):
        nulos_genes = self.uno(
            "SELECT COUNT(*) FROM genes "
            "WHERE especie IS NULL OR nombre IS NULL OR longitud IS NULL"
        )
        nulos_cultivos = self.uno(
            "SELECT COUNT(*) FROM cultivos WHERE cultivo IS NULL OR anio IS NULL "
            "OR produccion IS NULL OR rendimiento IS NULL"
        )
        self.assertEqual(nulos_genes + nulos_cultivos, 0)

    def test_cultivos_y_anios_distintos(self):
        self.assertEqual(self.uno("SELECT COUNT(DISTINCT cultivo) FROM cultivos"), 5)
        self.assertEqual(self.uno("SELECT COUNT(DISTINCT anio) FROM cultivos"), 3)


# 5.3 Validación de resultados de las consultas (pruebas funcionales)
class TestConsultas(BaseDB):
    def test_total_cultivos(self):
        self.assertEqual(self.uno("SELECT COUNT(*) FROM cultivos"), 15)

    def test_produccion_total(self):
        self.assertEqual(self.uno("SELECT SUM(produccion) FROM cultivos"), 60820000)

    def test_produccion_por_anio(self):
        filas = self.todos(
            "SELECT anio, SUM(produccion) FROM cultivos GROUP BY anio ORDER BY anio"
        )
        self.assertEqual(
            dict(filas), {2021: 19720000, 2022: 20240000, 2023: 20860000}
        )

    def test_rendimiento_promedio_cana(self):
        promedio = self.uno(
            "SELECT AVG(rendimiento) FROM cultivos WHERE cultivo = 'Caña de azúcar'"
        )
        self.assertAlmostEqual(float(promedio), 71.8333, places=3)

    def test_cultivo_mas_eficiente(self):
        cultivo = self.uno(
            "SELECT cultivo FROM cultivos GROUP BY cultivo "
            "ORDER BY AVG(rendimiento) DESC LIMIT 1"
        )
        self.assertEqual(cultivo, "Caña de azúcar")


if __name__ == "__main__":
    unittest.main(verbosity=2)