import pickle
import click

@click.command()
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    """Script to print humanreadable metadata"""    
    with open(path, 'rb') as f:
        data = pickle.load(f)
        for val in data:
            print("###")
            print(val)
            for key in data[val]:
                if key != "encoding":
                    print(key, ":", data[val][key])
