import os
from pathlib import Path

import click
import pydicom


def check_is_dir(p: Path):
    if not p.is_dir():
        click.echo(f"'{p}' is not a directory")
        exit(1)


def check_is_dicom_file(p: Path):
    if not p.is_file():
        click.echo(f"'{p} is not a file'")
        exit(0)
    ext = os.path.splitext(p)[-1].lower()
    if ext != '.dcm':
        click.echo(f"invalid file extension {ext}, expected .dcm")
        exit(1)


def check_is_anonymous(source: Path) -> None:
    dataset = pydicom.dcmread(source)
    pn = dataset.data_element('PatientName')
    pid = dataset.data_element('PatientID')
    if pn.value != "anonymous":
        click.echo(f"{source}: PatientName are not anonymous")
        exit(1)
    if pid.value != "anonymous":
        click.echo(f"{source}: PatientID are not anonymous")
        exit(1)
