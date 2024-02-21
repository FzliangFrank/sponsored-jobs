
import ibis
import pandas as pd
from .config import architect

class Driller:
    def __init__(self):
        print('a new driller created')
        super().__init__()

    def drill(self):
        pass

class Pipe:
    PROJECT='visa-sponsor-uk',
    DATASET='public'
    def __init__(self, table):
       
        self.table = table
        print(f'new pipe established to {self.table}')
        pass
    def connect(self):
        conn=ibis.bigquery.connect(
            project_id=self.PROJECT,
            dataset_id=self.DATASET
        )
        self.conn=conn

    def push(self, table: str, content: pd.DataFrame):
        self.validate(table, content)
        self.conn.insert(table, content)

    def validate(self):
        pass

class Job(Pipe, Driller):
    def __init__(self):
        super().__init__(table=architect.get('company_table'))
        
class Company(Pipe, Driller):
    def __init__(self):
        super().__init__(table = architect.get('company_table'))




