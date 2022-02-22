# Created 22.02.2022 :)

import argparse


class Args(argparse.Namespace):
    def __init__(self):
        super().__init__()
        self.command: str


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['github'])
    args: Args = parser.parse_args(namespace=Args())

    match args.command:
        case "github":
            print("OK")
        case _:
            raise ValueError(args.command)


if __name__ == "__main__":
    cli()
