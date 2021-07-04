from shutil import copy

from checks import *


@click.group()
def cli():
    """
    This is a CLI for manage and builds a DICOM datasets
    """
    pass


@cli.command()
@click.option('-r', '--recursive', is_flag=True, help='search recursively in SOURCE directory')
@click.argument('source')
def add_extension(recursive: bool, source: str):
    """adds .dcm extension to all files without extension

    DIRECTORY is the directory to find files without extension"""
    directory_path = Path(source)
    check_is_dir(directory_path)
    to_change = set()
    q = [directory_path]
    while q:
        current = q.pop(0)
        for item in [current / x for x in os.listdir(current)]:
            if item.is_file():
                ext = os.path.splitext(item)[-1].lower()
                if ext == "":
                    to_change.add(item)
            elif item.is_dir() and recursive:
                q.append(item)
    with click.progressbar(to_change) as bar:
        for item in bar:
            os.rename(item, f'{item}.dcm')


@cli.command(short_help='copy DICOM files to the new destination')
@click.option('-r', '--recursive', is_flag=True, help='search recursively in SOURCE directory')
@click.option('-p', '--prefix', default='Item_', help='set prefix to files when are copied')
@click.option('-s', '--start', default=1, help='set the counter or index start')
@click.argument('source')
@click.argument('destination')
def extract_dcm(recursive: bool, prefix: str, start: int, source: str, destination: str):
    """
    Copies all DICOM files from SOURCE to DESTINATION, the destination file
    format is DESTINATION/<prefix><index>.dcm
    """
    source_path = Path(source)
    check_is_dir(source_path)
    destination_path = Path(destination)
    check_is_dir(destination_path)

    to_copy = set()
    q = [source_path]
    while q:
        current = q.pop(0)
        for item in [current / x for x in os.listdir(current)]:
            if item.is_file():
                ext = os.path.splitext(item)[-1].lower()
                if ext == ".dcm":
                    to_copy.add(item)
            elif item.is_dir() and recursive:
                q.append(item)
    with click.progressbar(to_copy) as bar:
        for item in bar:
            copy(item, destination_path / f"{prefix}{start}.dcm")
            start += 1


@cli.command(short_help='anonymize DICOM files')
@click.option('-r', '--recursive', is_flag=True, help='search recursively in SOURCE directory')
@click.argument('source')
def anonymize(recursive: bool, source: str):
    """
    Anonymize all DICOM files in SOURCE, can be a file or a directory.
    If SOURCE is a directory, and --recursive option
    are enabled, then the search is made recursively in SOURCE.
    """

    def __anonymize_file__(f: Path):
        dataset = pydicom.dcmread(f)
        pn = dataset.data_element('PatientName')
        pid = dataset.data_element('PatientID')
        pn.value = "anonymous"
        pid.value = "anonymous"
        dataset.save_as(f)

    source_path = Path(source)
    if source_path.is_file():
        check_is_dicom_file(source_path)
        __anonymize_file__(source_path)
    elif source_path.is_dir():
        to_anonymize = set()
        q = [source_path]
        while q:
            current = q.pop(0)
            for item in [current / x for x in os.listdir(current)]:
                if item.is_file() and os.path.splitext(item)[-1].lower() == '.dcm':
                    to_anonymize.add(item)
                elif item.is_dir() and recursive:
                    q.append(item)
        with click.progressbar(to_anonymize) as bar:
            for item in bar:
                __anonymize_file__(item)


@cli.command(short_help='check if DICOM are already anonymous')
@click.option('-r', '--recursive', is_flag=True, help='search recursively in SOURCE directory')
@click.argument('source')
def is_anonymous(recursive: bool, source: str):
    """
    Check if DICOM files are anonymous in SOURCE, can be a file or a directory.
    If SOURCE is a directory, and --recursive option
    are enabled, then the check is made recursively in SOURCE.
    """
    source_path = Path(source)
    if source_path.is_file():
        check_is_anonymous(source_path)
        click.echo('True')
    elif source_path.is_dir():
        to_check = set()
        q = [source_path]
        while q:
            current = q.pop(0)
            for item in [current / x for x in os.listdir(current)]:
                if item.is_file():
                    to_check.add(item)
                elif item.is_dir() and recursive:
                    q.append(item)
        with click.progressbar(to_check) as bar:
            for item in bar:
                check_is_anonymous(item)
        click.echo('True')
