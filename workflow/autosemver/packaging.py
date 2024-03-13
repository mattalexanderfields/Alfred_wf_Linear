#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file was part of lago project.
# This file was part of INSPIRE-SCHEMAS.
# This file is part of autosemver.
# Copyright (C) 2014 Red Hat, Inc.
# Copyright (C) 2016 CERN.
# Copyright (C) 2016 David Caro.
#
# autosemver is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# autosemver is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autosemver; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
import os
import pkg_resources

from . import api


def get_current_version(project_name=None, project_dir=os.curdir,
                        repo_dir=None):
    """
    Retrieves the version of the package, checking in this order of priority:

    * From an environment variable named ${project_name}_VERSION (all in caps)
      if project_name was specified.
    * From the PKG-INFO file if inside a packaged distro.
    * From the git history.

    Args:
        project_name(str): Name of the project to get the version for, if none
            passed, will not use any environment variable override.

    Returns:
        str: Version for the package.

    Raises:
        RuntimeError: If the version could not be retrieved.
    """
    if project_name is not None:
        version_env_var = '%s_VERSION' % project_name.upper()

        if version_env_var in os.environ and os.environ[version_env_var]:
            return os.environ[version_env_var]

    version = None
    repo_dir = repo_dir or project_dir
    pkg_info_file = os.path.join(project_dir, 'PKG-INFO')
    if os.path.exists(pkg_info_file):
        with open(pkg_info_file) as info_fd:
            for line in info_fd.readlines():
                if line.startswith('Version: '):
                    version = line.split(' ', 1)[-1]

    if version is None:
        try:
            version = api.get_current_version(repo_path=repo_dir)
        except:
            pass

    if version is None:
        if project_name:
            try:
                distribution = pkg_resources.get_distribution(project_name)
                if distribution.has_version():
                    version = distribution.version
            except:
                pass

    if version is None:
        raise RuntimeError('Failed to get package version')

    # py3 compatibility step
    if not isinstance(version, str) and isinstance(version, bytes):
        version = api._to_str(version)

    return version


def get_authors(project_dir=os.curdir):
    """
    Retrieves the authors list, from the AUTHORS file (if in a package) or
    generates it from the git history.

    Returns:
        list(str): List of authors

    Raises:
        RuntimeError: If the authors could not be retrieved
    """
    authors = set()
    pkg_info_file = os.path.join(project_dir, 'PKG-INFO')
    authors_file = os.path.join(project_dir, 'AUTHORS')
    if os.path.exists(pkg_info_file) and os.path.exists(authors_file):
        with open(authors_file) as authors_fd:
            authors = set(authors_fd.read().splitlines())
    else:
        authors = api.get_authors(repo_path=project_dir)

    return authors


def get_changelog(project_dir=os.curdir, bugtracker_url='', rpm_format=False):
    """
    Retrieves the changelog, from the CHANGELOG file (if in a package) or
    generates it from the git history. Optionally in rpm-compatible format.

    :param project_dir: Path to the git repo of the project.
    :type project_dir: str
    :param bugtracker_url: Url to the bug tracker for the issues.
    :type bugtracker_url: str
    :param rpm_format: if set to True, will make the changelog rpm-compatible
    :returns: changelog
    :rtype: str
    :rises RuntimeError: If the changelog could not be retrieved
    """
    changelog = ''
    pkg_info_file = os.path.join(project_dir, 'PKG-INFO')
    changelog_file = os.path.join(project_dir, 'CHANGELOG')
    if os.path.exists(pkg_info_file) and os.path.exists(changelog_file):
        with open(changelog_file) as changelog_fd:
            changelog = changelog_fd.read()

    else:
        changelog = api.get_changelog(
            repo_path=project_dir,
            bugtracker_url=bugtracker_url,
            rpm_format=rpm_format,
        )

    return changelog


def get_releasenotes(project_dir=os.curdir, bugtracker_url=''):
    """
    Retrieves the release notes, from the RELEASE_NOTES file (if in a package)
    or generates it from the git history.

    Args:
        project_dir(str): Path to the git repo of the project.
        bugtracker_url(str): Url to the bug tracker for the issues.

    Returns:
        str: release notes

    Raises:
        RuntimeError: If the release notes could not be retrieved
    """
    releasenotes = ''
    pkg_info_file = os.path.join(project_dir, 'PKG-INFO')
    releasenotes_file = os.path.join(project_dir, 'RELEASE_NOTES')
    if os.path.exists(pkg_info_file) and os.path.exists(releasenotes_file):
        with open(releasenotes_file) as releasenotes_fd:
            releasenotes = releasenotes_fd.read()

    else:
        releasenotes = api.get_releasenotes(
            repo_path=project_dir,
            bugtracker_url=bugtracker_url,
        )

    return releasenotes


def create_authors(project_dir=os.curdir):
    """
    Creates the authors file, if not in a package.

    Returns:
        None

    Raises:
        RuntimeError: If the authors could not be retrieved
    """
    pkg_info_file = os.path.join(project_dir, 'PKG-INFO')
    authors_file = os.path.join(project_dir, 'AUTHORS')
    if os.path.exists(pkg_info_file):
        return

    authors = get_authors(project_dir=project_dir)
    with open(authors_file, 'wb') as authors_fd:
        authors_fd.write(
            b'\n'.join(a.encode('utf-8') for a in authors) + b'\n'
        )


def create_changelog(project_dir=os.curdir, bugtracker_url='',
                     rpm_format=False):
    """
    Creates the changelog file, if not in a package.

    :param project_dir: Path to the git repo of the project.
    :type project_dir: str
    :param bugtracker_url: Url to the bug tracker for the issues.
    :type bugtracker_url: str
    :param rpm_format: if set to True, will make the changelog rpm-compatible.
    :type rpm_format: bool
    :rises RuntimeError: If the changelog could not be retrieved
    """
    pkg_info_file = os.path.join(project_dir, 'PKG-INFO')
    if os.path.exists(pkg_info_file):
        return

    with open('CHANGELOG', 'wb') as changelog_fd:
        changelog_fd.write(
            get_changelog(
                project_dir=project_dir,
                bugtracker_url=bugtracker_url,
                rpm_format=rpm_format,
            ).encode('utf-8')
        )


def create_releasenotes(project_dir=os.curdir, bugtracker_url=''):
    """
    Creates the release notes file, if not in a package.

    Args:
        project_dir(str): Path to the git repo of the project.
        bugtracker_url(str): Url to the bug tracker for the issues.

    Returns:
        None

    Raises:
        RuntimeError: If the release notes could not be retrieved
    """
    pkg_info_file = os.path.join(project_dir, 'PKG-INFO')
    if os.path.exists(pkg_info_file):
        return

    with open('RELEASE_NOTES', 'wb') as releasenotes_fd:
        releasenotes_fd.write(
            get_releasenotes(
                project_dir=project_dir,
                bugtracker_url=bugtracker_url,
            ).encode('utf-8') + b'\n'
        )
