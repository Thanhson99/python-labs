"""argparse subcommand sample."""

import argparse


parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="cmd", required=True)

hello = sub.add_parser("hello")
hello.add_argument("--name", default="world")

sum_cmd = sub.add_parser("sum")
sum_cmd.add_argument("--a", type=int, required=True)
sum_cmd.add_argument("--b", type=int, required=True)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.cmd == "hello":
        print(f"hello {args.name}")
    elif args.cmd == "sum":
        print(args.a + args.b)
