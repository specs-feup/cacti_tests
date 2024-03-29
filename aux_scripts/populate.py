import os


def populate(path: str) -> None:
    """Provides the necessary files on the output directory

    Attributes:
        path (str): path to the output directory
    """

    file = open(path + "src.cpp", "x")
    file = open(path + "ir.ll", "x")
    file = open(path + "results.json", "x")


def get_immediate_subdirs(root: str) -> list[str]:
    """Returns the immediate subdirectories of the given root directory

    Attributes:
        root (str): the root directory

    Returns:
        list[str]: the immediate subdirectories of the given root directory
    """

    return [(root + name + '/') for name in os.listdir(root)
            if os.path.isdir(os.path.join(root, name))]


if __name__ == "__main__":
    dirs = [
        "./01_language/"
    ]

    for dir in dirs:
        sub_dirs = get_immediate_subdirs(dir)
        for sub_dir in sub_dirs:
            child_dirs = get_immediate_subdirs(sub_dir)
            for child_dir in child_dirs:
                populate(child_dir[:-1] + "/")
