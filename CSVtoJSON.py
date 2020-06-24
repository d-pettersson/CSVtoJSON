import csv
import json
import os
import argparse


def remove_header(csv_path, lines_to_remove):
    try:
        with open(csv_path, 'rt', encoding='utf-8') as source:
            reader = csv.reader(source)

            with open('tmp.csv', 'wt', encoding='utf-8') as output:
                writer = csv.writer(output)
                for i, row in enumerate(reader):
                    if i > lines_to_remove - 1:
                        writer.writerow(row)

    except IOError as err:
        print("I/O error: {0}".format(err))


def generate_labels(csv_path, prefix):
    try:
        with open(csv_path, 'rt', encoding='utf-8') as source:
            reader = csv.reader(source)
            headers = next(reader)
            return [label for label in headers if prefix not in label and label != '']

    except IOError as err:
        print("I/O error: {0}".format(err))


def create_dict(csv_path, text_id):
    data = {}
    try:
        with open(csv_path, 'rt', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                text_num = row[text_id]
                data[text_num] = row
        return data

    except IOError as err:
        print("I/O error: {0}".format(err))


def reduce_dict(data, labels):
    for keys in data:
        for label in labels:
            del data[keys][label]


def remove_prefix(data, prefix):
    res = dict()
    for key in data.keys():
        if isinstance(data[key], dict):
            res[key.strip().replace(prefix, '')] = remove_prefix(data[key], prefix)
        else:
            res[key.strip().replace(prefix, '')] = data[key]
    return res


def change_case(data):
    res = dict()
    for key in data.keys():
        if isinstance(data[key], dict):
            res[key.lower().strip()] = change_case(data[key])
        else:
            res[key.lower().strip()] = data[key]
    return res


def remove_empty_keys(data):
    res = dict()
    for key in data.keys():
        if key != '':
            if isinstance(data[key], dict):
                res[key] = remove_empty_keys(data[key])
            else:
                res[key] = data[key]
    return res


def empty_finder(data):
    with open('missing.txt', 'wt') as file:
        for k, v in data.items():
            for key, value in v.items():
                if not value:
                    file.write(' '.join((k, key, '\n')))


def export_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json_file.write(json.dumps(data, indent=4))


def main():
    description = 'This converts a CSV file to a JSON file. The missing dialogues are logged in the missing.txt file'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-c', '--csv_path', help='Path of the input csv', required=True, type=str)
    parser.add_argument('-j', '--json_path', help='Path of the output json', required=True, type=str)
    parser.add_argument('-p', '--prefix', help='Change the default text prefix. Default: TEXT', type=str)
    parser.add_argument('-rl', '--remove_lines', help='Number of lines to remove in the header. Default = 2', default=2, type=int)
    args = vars(parser.parse_args())

    tmp_path = 'tmp.csv'
    prefix = 'TEXT'
    text_id = 'TXT-NR'

    remove_header(args['csv_path'], args['remove_lines'])
    data = create_dict(tmp_path, text_id)
    labels = generate_labels(tmp_path, prefix)
    reduce_dict(data, labels)
    data = remove_empty_keys(data)
    export_json(change_case(remove_prefix(data, prefix)), args['json_path'])
    empty_finder(data)
    os.remove(tmp_path)


if __name__ == '__main__':
    main()
