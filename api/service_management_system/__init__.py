import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--dev", help="enable dev mode (uses local database)", action="store_true")

args = parser.parse_args()

IS_DEV = args.dev
