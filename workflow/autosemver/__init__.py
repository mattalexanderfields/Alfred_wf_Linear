# -*- coding: utf-8 -*-
#
# This file was part of lago project.
# This file was part of INSPIRE-SCHEMAS.
# This file is part of autosemver.
# Copyright (C) 2016 CERN.
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

import copy
import sys
import warnings

import argparse

from .api import (
    get_authors,
    get_changelog,
    get_current_version,
    get_releasenotes,
    tag_versions,
)
from .git import _to_str
from .packaging import (
    get_current_version as pkg_version,
    create_authors,
    create_changelog,
    create_releasenotes,
)

PROJECT_NAME = 'python-autosemver'


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'repo_path', help='Git repo to generate the changelog for.'
    )
    subparsers = parser.add_subparsers()
    changelog_parser = subparsers.add_parser('changelog')
    changelog_parser.add_argument(
        '--from-commit',
        default=None,
        help='Commit to start the changelog from'
    )
    changelog_parser.add_argument(
        '--rpm-format',
        action='store_true',
        help='If set, the changelog will be rpm friendly.'
    )
    changelog_parser.set_defaults(
        func=lambda *args, **kwargs: get_changelog(*args, **kwargs).strip()
    )
    version_parser = subparsers.add_parser('version')
    version_parser.set_defaults(func=get_current_version)
    releasenotes_parser = subparsers.add_parser('releasenotes')
    releasenotes_parser.add_argument(
        '--from-commit',
        default=None,
        help='Commit to start the release notes from.'
    )
    releasenotes_parser.set_defaults(func=get_releasenotes)
    authors_parser = subparsers.add_parser('authors')
    authors_parser.add_argument(
        '--from-commit',
        default=None,
        help='Commit to start the authors from.'
    )
    authors_parser.set_defaults(
        func=lambda *args, **kwargs: '\n'.join(get_authors(*args, **kwargs))
    )
    tag_parser = subparsers.add_parser('tag')
    tag_parser.set_defaults(func=tag_versions)
    args = parser.parse_args(args)

    params = copy.deepcopy(vars(args))
    params.pop('func')

    print(_to_str(args.func(**params)))


def distutils_default_case(metadata, attr, value):
    if value:
        setattr(metadata, attr, value)

    return metadata


def distutils_autosemver_case(
    metadata, with_release_notes=False, with_authors=True, with_changelog=True,
    bugtracker_url=None,
):
    """
    :param metadata: distutils metadata object.
    :param with_release_notes: if true, will create the release notes.
    :type with_release_notes: bool
    :param with_authors: if true, will create the authors file.
    :type with_authors: bool
    :param with_changelog: if true, will create the release notes file.
    :type with_changelog: bool
    :param bugtracker_url: URL for the bugtracker of the project.
    :type bugtracker_url: str
    :returns metadata: the updated distutils metadata.
    """
    metadata.version = pkg_version()
    if with_authors:
        create_authors()

    if with_release_notes:
        create_releasenotes()

    if with_changelog:
        create_changelog()

    metadata._autosmever = True

    return metadata


def distutils_old_autosemver_case(metadata, attr, value):
    """DEPRECATED"""
    metadata = distutils_default_case(metadata, attr, value)
    create_changelog(bugtracker_url=getattr(metadata, 'bugtracker_url', ''))
    return metadata


def distutils(dist, attr, value):
    if attr != 'autosemver':
        dist.metadata = distutils_default_case(
            metadata=dist.metadata,
            attr=attr,
            value=value,
        )
    if attr == 'bugtracker_url':
        warnings.warn(
            'Using explicit parametes is deprecated and will be removed, '
            'pass a dictionary as the value of the autosemver parameter '
            'instead.'
        )

        if getattr(dist.metadata, '_autosmever', False):
            dist.metadata = distutils_old_autosemver_case(
                metadata=dist.metadata,
                attr=attr,
                value=value,
            )

    else:
        if not isinstance(value, dict):
            value = {
                'bugtracker_url': getattr(dist.metadata, 'bugtracker_url', ''),
            }

        dist.metadata = distutils_autosemver_case(
            metadata=dist.metadata,
            **value
        )

    return
