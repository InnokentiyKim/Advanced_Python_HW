def flat_generator(list_of_lists):
    for item in list_of_lists:
        yield from item


def common_flat_generator(list_of_lists):
    for inner in list_of_lists:
        if not hasattr(inner, '__iter__') or type(inner) is str:
            yield inner
        else:
            yield from common_flat_generator(inner)
