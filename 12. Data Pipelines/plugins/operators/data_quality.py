from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 conn_id = "",
                 checks = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)

        self.conn_id = conn_id
        self.checks = checks
        

    def execute(self, context):
        self.log.info('DataQualityOperator not implemented yet')
        hook = PostgresHook(self.conn_id)
        
        for check in self.checks:
            self.log.info(f'Running query: "{sql}"')
            check.records = hook.get_records(sql)
            result = check.validate()
