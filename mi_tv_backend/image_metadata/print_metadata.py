import pickle
import click

@click.command()
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    """Script to print humanreadable metadata"""    
    with open(path, 'rb') as f:
        data = pickle.load(f)
        print(data)
