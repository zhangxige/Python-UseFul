import argparse


# 简单的命令行计算器 demo
def main():
    parser = argparse.ArgumentParser(
        prog='Calculator',
        description='A simple command-line calculator',
        epilog='Example: python Argparse_Utils.py 10 5 --operation add'
    )
    parser.add_argument('num1', type=float, help='First number')
    parser.add_argument('num2', type=float, help='Second number')
    parser.add_argument('--operation',
                         choices=['add', 'subtract', 'multiply', 'divide'],
                         default='add',
                         help='Operation to perform (default: add)')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    num1 = args.num1
    num2 = args.num2
    operation = args.operation

    if operation == 'add':
        result = num1 + num2
        op_symbol = '+'
    elif operation == 'subtract':
        result = num1 - num2
        op_symbol = '-'
    elif operation == 'multiply':
        result = num1 * num2
        op_symbol = '*'
    elif operation == 'divide':
        if num2 == 0:
            print("Error: Division by zero!")
            return
        result = num1 / num2
        op_symbol = '/'

    if args.verbose:
        print(f"Performing: {num1} {op_symbol} {num2} = {result}")
    else:
        print(result)


if __name__ == '__main__':
    main()
