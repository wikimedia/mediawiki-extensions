#!/usr/bin/env python

import logging
import os.path
import subprocess

# Configuration
basepath = "mediawiki/extensions/"
gerrit_conf = {
    'host': 'gerrit.wikimedia.org',
    'port': '29418',
    'url': 'https://{host}/r/{project}'
    }

# Global logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def main():
    log.info("Fetching projects from gerrit (prefix: %s)" % basepath)
    projects = gerrit('ls-projects', ['-p', basepath]).splitlines()

    # strip out subprojects in extensions
    projects = [p for p in projects if '/' not in project_basename(p)]

    projects.sort()

    log.info("Checking modules")
    for p in projects:
        basename = project_basename(p)
        if not os.path.isdir(basename):
            log.info("Adding submodule for %s" % p)
            try:
                submodule_add(p)
            except subprocess.CalledProcessError:
                log.error("Git reported an issue adding module %s" % p)

    log.info("Rewriting .gitmodules")
    f = open('.gitmodules', 'w')
    f.write(generate_gitmodules(projects))
    f.close()

    log.info("Review change and submit!\nDone")


def submodule_add(project):
    cmd = 'git submodule add'.split(' ') + [
        gerrit_url(project),
        project_basename(project)
        ]
    subprocess.check_call(cmd)


def generate_gitmodules(projects):
    "Create a .gitmodules file with branch=."
    gitmodules = ''
    for project in projects:
        p_url = gerrit_url(project)
        gitmodules += (
            "[submodule \"{name}\"]\n"
            "\tpath = {name}\n"
            "\turl = {url}\n"
            "\tbranch = .\n"
            ).format(
            name=project_basename(project),
            url=p_url
            )

    return gitmodules


def gerrit(gerrit_cmd, args=[], gerrit_conf=gerrit_conf):
    "Helper to execute a gerrit command."
    ssh = [
        '/usr/bin/ssh',
        '-p', gerrit_conf['port'],
        gerrit_conf['host'],
        ]

    cmd = ssh + ['gerrit {gerrit_cmd} {args}\''.format(
        ssh=ssh, gerrit_cmd=gerrit_cmd, args=' '.join(args))]

    return subprocess.check_output(cmd)


def gerrit_url(project):
    return gerrit_conf['url'].format(
        host=gerrit_conf['host'], project=project)


def project_basename(project):
    return project[len(basepath):]


if __name__ == '__main__':
    main()
