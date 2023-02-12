import csv
import re


def main():
    domain_references = 'Maquet.Domain.Barco.Contracts_Advanced-Find-Usages_and-Textual-Occurrences - ' +\
                          'with-errors-when-reference-to-Barco-is-removed.txt'
    framework_references = 'Maquet.Domain.BARCO-n-Contracts_Dependent-Modules - ' +\
                             'with-errors-when-reference-to-BARCO-is-removed.txt'

    obtain_input(domain_references, framework_references)

    records = load_csv(domain_references, framework_references)

    ignored_references = ['Barco', 'Contracts', 'Framework']
    scrub_records(records, ignored_references)

    dependencies = group_dependencies(records)

    format_output(dependencies, "out.txt")


def obtain_input(*filenames):
    for filename in filenames:
        references = normalize('raw_input/' + filename)
        save_normalized(references, 'csv_input/' + filename)


def normalize(filepath):
    module_pattern = r"\+\<(.*)\>"

    # Matches e.g.:
    # Error	CS0234	The type or namespace name '
    # Error	CS0103	The name '
    error_pattern = r"Error\s+CS[0-9]{4}\s+The[a-z ]+name '"

    def get_first_quoted_substring(message: str) -> str:
        begin = message.find("'") + 1
        end = message.find("'", begin)
        return message[begin:end]

    modulename = None
    dependencies = []
    with open(filepath) as file:
        for line in file:
            match = re.search(module_pattern, line)
            if match:
                modulename = match.group(1)
                continue

            if not re.match(error_pattern, line):
                continue

            dependencies.append([modulename, get_first_quoted_substring(line)])

    return dependencies


def save_normalized(references, filepath):
    with open(filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for line in references:
            csvwriter.writerow(line)


def load_csv(*filenames):
    records = []
    for filename in filenames:
        with open('csv_input/' + filename) as csvfile:
            csvreader = csv.reader(csvfile)
            for line in csvreader:
                record = (line[0], line[1])
                records.append(record)

    return records


def scrub_records(records, ignored_references):
    i = 0
    while i < len(records):
        reference = records[i][1]
        if any(ignored == reference for ignored in ignored_references):
            records.pop(i)
            continue

        i += 1


def group_dependencies(records):
    dependencies = {}
    for record in records:
        (module, reference) = record
        modules = dependencies.get(reference)
        if modules is None:
            modules = set()
            dependencies[reference] = modules

        modules.add(module)

    return dependencies


def format_output(dependencies, out_file):
    with open(out_file, 'w') as out:
        for dependency in sorted(dependencies.keys()):
            modules = dependencies[dependency]
            sorted_modules_list1 = "\n\t".join(sorted(modules))
            out.write(f"{dependency}:\n\t{sorted_modules_list1}\n\n")


if __name__ == '__main__':
    main()
