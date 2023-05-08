from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 conn_id = "",
                 checks = "",
                 sql = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)

        self.conn_id = conn_id
        self.checks = checks
        self.sql = sql

    def execute(self, context):
        self.log.info('LoadFactOperator start')
        hook = PostgresHook(self.conn_id)
        
        
