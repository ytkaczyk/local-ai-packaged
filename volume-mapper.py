from ruamel.yaml import YAML, CommentedMap as OrderedDict
import argparse
import os

def add_root_to_volumes(input: str, output:str, root_path: str):
    yaml=YAML(typ='rt')   # default, if not specfied, is 'rt' (round-trip)
    with open(input, "r") as file:
        data = yaml.load(file)

    for volume in data.get('volumes'):
        if data["volumes"][volume] is None:
            data["volumes"][volume]=OrderedDict({
                "driver": "local",
                "driver_opts": OrderedDict({
                    "type": "none",
                    "o": "bind",
                    "device": os.path.join(root_path, volume)
                })
            })

    with open(output, "w") as file:
        yaml.dump(data, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("--input", type=str, default="./docker-compose.yml", help="Input YAML file")
    parser.add_argument("--output", type=str, default="./docker-compose2.yml", help="Output YAML file")
    parser.add_argument("--root", type=str, default="/var/localai", help="Root path for volume mapping")
    args = parser.parse_args()

    add_root_to_volumes(args.input, args.output, args.root)