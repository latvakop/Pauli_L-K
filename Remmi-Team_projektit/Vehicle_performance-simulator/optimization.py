# Made by: Jesper Granat

from main import calculate_result


MAX_ITERS = 50


def diff(f, diff_pos, *args, h=0.001):
    """Differentiate numerically f w.r.t args[diff_pos]"""
    min_args = [arg for arg in args]
    min_args[diff_pos] -= h
    max_args = [arg for arg in args]
    max_args[diff_pos] += h
    p = args[diff_pos]

    return (f(*max_args) - f(*min_args)) / (2 * p)


def gradient(f, *args):
    """Calculate the gradient of function f with the parameters in *args"""
    return [diff(f, i, *args) for i in range(len(args))]


def gradient_descent(f, init_x=12.97, init_y=35.688, mu=10):
    next_y = init_y
    next_x = init_x
    for _ in range(MAX_ITERS):
        x = next_x
        y = next_y
        g = gradient(f, x, y)
        next_x = x - mu * g[0]
        next_y = y - mu * g[1]
    print(next_x, next_y)
    return next_x, next_y


def main():
    gradient_descent(calculate_result)


if __name__ == '__main__':
    main()
