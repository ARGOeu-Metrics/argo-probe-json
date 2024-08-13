from distutils.core import setup

NAME = "argo-probe-json"


def get_ver():
    try:
        for line in open(NAME + '.spec'):
            if "Version:" in line:
                return line.split()[1]

    except IOError:
        raise SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    author="SRCE",
    author_email="kzailac@srce.hr",
    description="ARGO probe that checks JSON response given the URL",
    url="https://github.com/ARGOeu-Metrics/argo-probe-json",
    package_dir={'argo_probe_json': 'modules'},
    packages=['argo_probe_json'],
    data_files=[('/usr/libexec/argo/probes/json', ['src/check_json'])]
)
