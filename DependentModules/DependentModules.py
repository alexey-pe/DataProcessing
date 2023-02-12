import csv
import re


def main():
    domainInputFileName = 'Maquet.Domain.Barco.Contracts_Advanced-Find-Usages_and-Textual-Occurrences - ' +\
                          'with-errorrs-when-reference-to-Barco-is-removed.txt'
    frameworkInputFileName = 'Maquet.Domain.BARCO-n-Contracts_Dependent-Modules - ' +\
                             'with-errors-when-reference-to-BARCO-is-removed.txt'

    obtain_input(domainInputFileName, frameworkInputFileName)

    # with open('csv_input/' + domainInputFileName) as normfile:
    #     for line in normfile:
    #         print(line)

    records = load_csv(domainInputFileName, frameworkInputFileName)

    # records = scrub_records(records)

    dependencies = group_dependencies(records)

    format_output(dependencies, "out.txt")


def obtain_input(*infiles):
    for infile in infiles:
        references = normalize('raw_input/' + infile)
        save_normalized(references, 'csv_input/' + infile)


def normalize(filename):
    modulepattern = r"\+\<(.*)\>"

    # Matches e.g.:
    # Error	CS0234	The type or namespace name '
    # Error	CS0103	The name '
    errorpattern = "Error\s+CS[0-9]{4}\s+The[a-z ]+name '"

    def GetFirstSingleQuotesContents(message: str) -> str:
        begin = message.find("'") + 1
        end = message.find("'", begin)
        return message[begin:end]

    modulename = None
    dependencies = []
    with open(filename) as rawfile:
        for line in rawfile:
            modulematch = re.search(modulepattern, line)
            if modulematch:
                modulename = modulematch.group(1)
                continue

            if not re.match(errorpattern, line):
                continue

            dependencies.append([modulename, GetFirstSingleQuotesContents(line)])

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


def group_dependencies(records):
    dependencies = {}
    for record in records:
        module = record[0]
        dependency = record[1]
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
