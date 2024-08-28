import click
from db_tool.data_processing import process_data
from db_tool.cache import Cache
from db_tool.ml_models import train_model as train_model_func, predict as predict_func
from db_tool.real_time import stream_data
from db_tool.compliance import check_compliance
from db_tool.unstructured_data import process_unstructured_data
from db_tool.automation import setup_cron_job, remove_cron_job

@click.group()
def cli():
    pass

# Data processing commands
@cli.command()
@click.option('--file_path', required=True, help='Path to the data file.')
@click.option('--operation', required=True, type=click.Choice(['clean', 'transform', 'visualize']), help='Data operation to perform.')
def data_process(file_path, operation):
    process_data(file_path, operation)

# Cache commands
@cli.command()
@click.option('--key', required=True, help='Key to set in the cache.')
@click.option('--value', required=True, help='Value to set in the cache.')
def cache_set(key, value):
    cache = Cache()
    cache.set(key, value)
    click.echo(f'Value set in cache: {value}')

@cli.command()
@click.option('--key', required=True, help='Key to retrieve from the cache.')
def cache_get(key):
    cache = Cache()
    value = cache.get(key)
    if value:
        click.echo(value)
    else:
        click.echo('Key not found in cache.')

@cli.command()
@click.option('--key', required=True, help='Key to delete from the cache.')
def cache_delete(key):
    cache = Cache()
    cache.delete(key)
    click.echo(f'Key {key} deleted from cache.')

# Machine learning commands
@cli.command()
@click.option('--file_path', required=True, help='Path to the data file for training.')
@click.option('--model_type', required=True, type=click.Choice(['linear_regression']), help='Type of model to train.')
@click.option('--target_column', required=True, help='Target column for the model.')
def train_model(file_path, model_type, target_column):
    train_model_func(file_path, model_type, target_column)

@cli.command()
@click.option('--model_path', required=True, help='Path to the trained model file.')
@click.option('--data_path', required=True, help='Path to the data file for prediction.')
def predict(model_path, data_path):
    predict_func(model_path, data_path)

# Real-time streaming command
@cli.command()
@click.option('--source', required=True, help='Path to the streaming data source.')
@click.option('--processing_logic', required=True, help='Processing logic for the stream.')
@click.option('--format', required=True, type=click.Choice(['csv', 'json']), help='Format of the streaming data.')
def stream(source, processing_logic, format):
    stream_data(source, processing_logic, format)

# Compliance check command
@cli.command()
@click.option('--data_path', required=True, help='Path to the data file for compliance check.')
@click.option('--compliance_type', required=True, type=click.Choice(['gdpr', 'hipaa']), help='Type of compliance to check.')
def compliance(data_path, compliance_type):
    check_compliance(data_path, compliance_type)

# Unstructured data processing command
@cli.command()
@click.option('--file_path', required=True, help='Path to the unstructured data file.')
@click.option('--data_type', required=True, type=click.Choice(['text', 'image']), help='Type of unstructured data.')
def unstructured_process(file_path, data_type):
    process_unstructured_data(file_path, data_type)

# Automation commands
@cli.command()
@click.option('--script_path', required=True, help='Path to the script to automate.')
@click.option('--schedule', required=True, help='Cron schedule for the automation.')
def automate(script_path, schedule):
    setup_cron_job(script_path, schedule)

@cli.command()
@click.option('--script_path', required=True, help='Path to the script to remove from automation.')
def automate_remove(script_path):
    remove_cron_job(script_path)

if __name__ == '__main__':
    cli()

