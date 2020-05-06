
def update_sample_name(sample_name: str):
    """
    Update sample name to remove file name if directory name present e.g.
    'dir_name | filename' becomes 'dirname'.
    """
    if "|" in sample_name:
        return "|".join(sample_name.split("|")[:-1])
    return sample_name