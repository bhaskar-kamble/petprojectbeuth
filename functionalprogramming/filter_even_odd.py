# functional programming
# given a list of integers, filter the even integers and the odd integers

def filter_function(to_be_filtered):

    even = list(filter(lambda x: x % 2 == 0, to_be_filtered))
    odd = list(filter(lambda x: x % 2 == 1, to_be_filtered))
    print("even numbers:")
    print(even)
    print("odd numbers:")
    print(odd)


if __name__ == '__main__':
    to_be_filtered = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter_function(to_be_filtered)
