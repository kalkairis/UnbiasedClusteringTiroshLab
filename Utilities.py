from os.path import join


def join_paths(paths):
    ret = ''
    for path in paths:
        if len(ret) == 0:
            ret = path
        else:
            ret = join(ret, path)
    return ret
