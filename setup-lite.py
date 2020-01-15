import os
import sys
import platform
import subprocess
import time

from setuptools import find_packages, setup


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


MAJOR = 0
MINOR = 1
PATCH = ''
SUFFIX = 'rc0'
SHORT_VERSION = '{}.{}.{}{}'.format(MAJOR, MINOR, PATCH, SUFFIX)

version_file = 'mmskeleton/version.py'


def get_git_hash():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        sha = out.strip().decode('ascii')
    except OSError:
        sha = 'unknown'

    return sha


def get_hash():
    if os.path.exists('.git'):
        sha = get_git_hash()[:7]
    elif os.path.exists(version_file):
        try:
            from mmskeleton.version import __version__
            sha = __version__.split('+')[-1]
        except ImportError:
            raise ImportError('Unable to get git version')
    else:
        sha = 'unknown'

    return sha


def write_version_py():
    content = """# GENERATED VERSION FILE
# TIME: {}
__version__ = '{}'
short_version = '{}'
mmskl_home = '{}'
"""
    sha = get_hash()
    VERSION = SHORT_VERSION + '+' + sha
    MMSKELETON_HOME = os.path.dirname(os.path.realpath(__file__))

    with open(version_file, 'w') as f:
        f.write(
            content.format(time.asctime(), VERSION, SHORT_VERSION,
                           MMSKELETON_HOME))


def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


def get_requirements(filename='requirements.txt'):
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, filename), 'r') as f:
        requires = [line.replace('\n', '') for line in f.readlines()]
    return requires


if __name__ == '__main__':
    write_version_py()
    setup(name='mmskeleton',
          version=get_version(),
          scripts=['./tools/mmskl'],
          description='Open MMLab Skeleton-based Human Understanding Toolbox',
          long_description=readme(),
          keywords='computer vision, human understanding, action recognition',
          url='https://github.com/open-mmlab/mmskeleton',
          packages=find_packages(exclude=('configs', 'tools', 'demo')),
          package_data={'mmskeleton.ops': ['*/*.so']},
          classifiers=[
              'Development Status :: 4 - Beta',
              'License :: OSI Approved :: Apache Software License',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
          ],
          license='Apache License 2.0',
          setup_requires=['pytest-runner'],
          tests_require=['pytest'],
          install_requires=get_requirements(),
          zip_safe=False)