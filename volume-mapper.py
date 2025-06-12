from ruamel.yaml import YAML, CommentedMap as OrderedDict, CommentedSeq as OrderedList

def main():
    yaml=YAML(typ='rt')   # default, if not specfied, is 'rt' (round-trip)
    with open("./docker-compose.yml", "r") as file:
        data = yaml.load(file)
    print(data)

    for volume in data.get('volumes'):
        if data["volumes"][volume] is None:
            data["volumes"][volume]=OrderedDict({
                "driver": "local",
                "driver_opts": OrderedDict({
                    "type": "none",
                    "o": "bind",
                    "device": f"/var/localai/{volume}"
                })
            })

    with open("./docker-compose2.yml", "w") as file:
        yaml.dump(data, file)

if __name__ == "__main__":
    main()