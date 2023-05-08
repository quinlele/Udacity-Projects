from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                conn_id = "",
                checks = "",
                sql = "",
                trunc=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        
        self.conn_id = conn_id
        self.checks = checks
        self.sql = sql
        self.trunc = trunc

    def execute(self, context):
        self.log.info('LoadDimensionOperator not implemented yet')
        hook = PostgresHook(self.conn_id)
        
        if self.trunc:
            self.log.info(f'Truncating table: {self.table}')
            hook.run(f'LoadDimensionOperator truncate {self.table}')

        self.log.info(f'Loading dimension table {self.table}')
        format_sql = f"INSERT INTO {self.sql}"
        
        hook.run(format_sql)
