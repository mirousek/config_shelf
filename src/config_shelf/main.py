import argparse
import os
import imp
from config_shelf import FileDefinition
from core.env_detectors import BaseEnvDetector
from core.writers import BaseWriter

__author__ = 'miroslav.stepanek'

from git import Repo, GitDB

def main(test=None):
    if test is None:
        parser = argparse.ArgumentParser(description='Run configuration changes.')
        parser.add_argument('--test', dest='test', action='store_const',
                           const=True, default=False,
                           help='Set test values (default: test defined values)')

        args = parser.parse_args()
        test = args.test

    # Populate path info
    repo = Repo('.', odbt=GitDB)
    wd = repo.working_dir
    wd = os.path.normcase(wd)
    components = []
    rest = wd
    print("Git root: " + wd)
    drive, rest = os.path.splitdrive(rest)

    rest2, tail = os.path.split(rest)
    if len(tail) == 0:
        rest = rest2

    while True:
        rest, tail = os.path.split(rest)
        if len(tail) > 0:
            components.append(tail)
        else:
            break

    definitions_file = os.path.join(wd, 'conf/config_shelf/definitions/config_shelf_file.py')
    definitions_file = os.path.normpath(definitions_file)
    print("Definitions file: " + definitions_file)
    definitions = imp.load_source('definitions', definitions_file)
    env_detector = definitions.EnvDetector()
    env_detector.git_root = wd
    env_detector.path_drive = drive
    env_detector.path_components = components
    env_detector.is_jenkins = components[0] == 'workspace'

    # Detect environment
    environment_result = env_detector.detect()
    if type(environment_result) is tuple:
        environment = environment_result[0]
        environment_params = environment_result[1:] if len(environment_result) > 1 else None
    else:
        environment, environment_params = environment_result, None

    print("env: {0} ({1})".format(environment, environment_params))

    # Update configuration

    definer = definitions.ConfigDefiner()
    definer.define()

    values_source = definitions.ValuesSource()
    if environment_params:
        values_source.generate_values(environment, *environment_params)
    else:
        values_source.generate_values(environment)

    FileDefinition.base_path = wd
    for k, v in definer.defs.items():
        # value = 'prase.mirousek.eu'
        value = getattr(values_source, k)
        if test:
            value = '**********'
        # for v2 in v.targets:
        if isinstance(v, BaseWriter):
            v.write(value)
        else:
            for v2 in v:
                v2.write(value)

if __name__ == '__main__':
    main()
