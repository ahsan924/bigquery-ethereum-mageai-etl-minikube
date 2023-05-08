from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path
from mage_ai.data_preparation.variable_manager import set_global_variable
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'ethereum'  # Specify the name of the schema to export data to
    table_name = 'token_transfers'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    print('Loading Data to DB..')

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            allow_reserved_words=True,
            index=False,  # Specifies whether to include index in exported table
            if_exists='append',  # Specify resolution policy if table name already exists
            unique_conflict_method='UPDATE',
            unique_constraints=['transaction_hash', 'log_index']
        )

#  After first successfull execution update is_tokens_first_run='False'
    # set_global_variable('daily_ethereum_pipeline', 'is_token_transfers_first_run', 'False')