from data.utils.terminal_colors import error


def get_or_error(patch_data, key: str):
    if patch_data.get(key, None) is None:
        error(f"key \'{key}\' not specified")
        exit(1)

    return patch_data[key]