import csv
import re


def main():
    domain_dependencies = 'Maquet.Domain.Barco.Contracts_Advanced-Find-Usages_and-Textual-Occurrences - ' +\
                          'with-errors-when-reference-to-Barco-is-removed.txt'
    framework_dependencies = 'Maquet.Domain.BARCO-n-Contracts_Dependent-Modules - ' +\
                             'with-errors-when-reference-to-BARCO-is-removed.txt'

    obtain_input(domain_dependencies, framework_dependencies)

    records = load_csv(domain_dependencies, framework_dependencies)

    ignored_dependencies = ['Barco', 'Contracts', 'Framework']
    scrub_records(records, ignored_dependencies)

    dependencies = group_dependencies(records)

    format_output(dependencies, "out.txt")


def obtain_input(*files):
    for file in files:
        references = normalize('raw_input/' + file)
        save_normalized(references, 'csv_input/' + file)


def normalize(filename):
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
    with open(filename) as file:
        for line in file:
            match = re.search(module_pattern, line)
            if match:
                modulename = match.group(1)
                continue

            if not re.match(error_pattern, line):
                continue

            dependencies.append([modulename, get_first_quoted_substring(line)])

    return dependencies


def save_normalized(references, filename):
    with open(filename, 'w', newline='') as csvfile:
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


def scrub_records(records, ignored_dependencies):
    i = 0
    while i < len(records):
        dependency = records[i][1]
        if any(ignored == dependency for ignored in ignored_dependencies):
            records.pop(i)
            continue

        i += 1


def group_dependencies(records):
    dependencies = {}
    for record in records:
        (module, dependency) = record
        modules = dependencies.get(dependency)
        if modules is None:
            modules = set()
            dependencies[dependency] = modules

        modules.add(module)

    return dependencies


def format_output(dependencies, out_file):
    with open(out_file, 'w') as out:
        for dependency in dependencies.keys():
            modules = ", ".join(sorted(dependencies[dependency]))
            out.write(f"{dependency}: {modules}\n")


if __name__ == '__main__':
    main()
