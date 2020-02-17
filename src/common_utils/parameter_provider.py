import sys

from configuration import Configuration


def return_parameter_value(parameter):
    return Configuration[parameter].value


def main(requested_parameter):
    res = return_parameter_value(requested_parameter)
    sys.stderr.write(str(res))
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
