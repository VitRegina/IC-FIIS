import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host="localhost",
            database="FUNDOS",
            user="postgres",
            password="ifsp"
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        fundo_nome = "ITAÚ ASSET RURAL FIAGRO - IMOBILIÁRIO"
        fundo_codigo = "ITAÚ-ASSET-COD"  

        self.cur.execute("SELECT id FROM public.fundo WHERE codigo_fundo = %s", (fundo_codigo,))
        result = self.cur.fetchone()
        if result:
            fundo_id = result[0]
        else:
            self.cur.execute(
                "INSERT INTO public.fundo (codigo_fundo, nome_fundo) VALUES (%s, %s) RETURNING id",
                (fundo_codigo, fundo_nome)
            )
            fundo_id = self.cur.fetchone()[0]
            self.conn.commit()


        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, "%d/%m/%Y").date()
            except:
                return None

        valor_provento = float(item.get('valor do provento', '0').replace(',', '.'))
        data_pagamento = parse_date(item.get('data do pagamento', ''))
        data_base = parse_date(item.get('Data-base', ''))
        periodo_referencia = parse_date(item.get('período de referência', ''))

        self.cur.execute("""
            INSERT INTO public.provento (fundo_id, valor_provento, data_pagamento, data_base, periodo_referencia, id_fundo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (fundo_id, valor_provento, data_pagamento, data_base, periodo_referencia, fundo_id)
        )
        self.conn.commit()

        return item
