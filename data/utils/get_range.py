from data.utils.errors import AttributeInvalidError


def get_range(range_str: str) -> set[int]:
    output_range = []
    for range_or_num in [x.strip() for x in range_str.split(',')]:
        if '-' in range_or_num:
            start = int(range_or_num.split('-')[0])
            end = int(range_or_num.split('-')[1])
            if start > end:
                raise AttributeInvalidError(f"Invalid range: start {start} must be less than end {end}")
            for i in range(start, end+1):
                output_range.append(i)
        else:
            output_range.append(int(range_or_num))

    output_range.sort()
    return set(output_range)