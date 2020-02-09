import time
import datetime as dt
import os
import sys
import subprocess
from pprint import pprint

import click
import requests



def global_site_package_directory():
    return os.path.expanduser('~/.mpip')


GLOBAL_STORE = global_site_package_directory()


if not os.path.exists(GLOBAL_STORE):
    os.makedirs(GLOBAL_STORE)


def get_latest_version(package):
    url = 'https://pypi.org/simple/{}'.format(package)
    response = requests.get(url)
    data = response.text
    pprint(data)


def get_target_dir(package):
    py_version = sys.version_info
    if '==' in package:
        package_name, package_version = package.split('==')
    else:
        package_name = package
        package_version = get_latest_version(package_name)

    index = '{}.{}_{}'.format(py_version.major, py_version.minor, package_version)
    target = os.path.join(GLOBAL_STORE, package_name, index)
    return target



def link_package(package, target_dir):
    pass


def install_package(package):
    print('Installing {}'.format(package))
    target_dir = get_target_dir(package)
    print(target_dir)
    if not os.path.exists(target_dir):
        cmd = 'python -m pip install --target {} {}'.format(target_dir, package)
        print(cmd)
        os.system(cmd)
    link_package(package, target_dir)

@click.group()
@click.pass_context
def group(ctx):
    pass


@group.command()
@click.option('-r', '--requirements', required=False)
@click.argument('package', required=False)
def install(package=None, requirements=None):
    """
    Install a package
    """
    if requirements:
        with open(requirements) as fh:
            packages = fh.readlines()
        for package in packages:
            install_package(package.strip())
    else:
        install_package(package)
