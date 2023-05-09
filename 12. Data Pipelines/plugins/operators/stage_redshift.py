from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 conn_id = "",
                 checks = "",
                 aws_credentials_id = "",
                 s3_bucket = "",
                 s3_key = "",
                 region = "",
                 table = "",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        
        self.conn_id = conn_id
        self.checks = checks
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region

    def execute(self, context):
        self.log.info('StageToRedshiftOperator start')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        hook = PostgresHook(self.conn_id)

        format_sql = StageToRedshiftOperator.copy_sql.format(
            self.table, s3_path, credentials.access_key,
            credentials.secret_key, self.region)
   
        

        hook.run(format_sql)
        self.log.info(
            f"StageToRedshiftOperator finish copy - {self.table}")





