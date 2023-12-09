import argparse


# argparse 相关
def argparse_test():
    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='What the program does',
                        epilog='Text at the bottom of help')
    parser.add_argument('filename')           # positional argument
    parser.add_argument('-c', '--count')      # option that takes a value
    parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--batch', type=int, default=4)
    args = parser.parse_args()
    print(args.filename, args.count, args.verbose)


if __name__ == '__main__':
    argparse_test()
    pass
