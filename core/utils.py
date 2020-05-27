import re


def transform_data(data: list):
    for idx, link in enumerate(data):
        if link.startswith(('http://', 'https://')):
            data[idx] = re.findall(r'\w+.\w+', link.split('http')[1])[0]
        else:
            data[idx] = re.findall(r'\w+.\w+', link)[0]
    return data
