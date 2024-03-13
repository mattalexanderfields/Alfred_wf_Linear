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
# along with INSPIRE-SCHEMAS; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""
Script to generate the version, changelog and releasenotes from the git
repository.
"""
from __future__ import print_function

import sys

from collections import OrderedDict
from functools import wraps

WITH_GIT = True
try:
    import dulwich.repo
    import dulwich.walk
except ImportError:
    WITH_GIT = False

PYTHON_34 = (
    sys.version_info.major == 3 and
    sys.version_info.minor == 4
)

if PYTHON_34:
    # In python 3.4 the reversed function needs a strict sequence.
    old_reversed = reversed

    def reversed(sequence):
        return old_reversed(list(sequence))


from .git import (  # noqa
    _to_str,
    get_tags,
    get_refs,
    get_children_per_first_parent,
    get_repo_object,
    get_version,
    fuzzy_matches_refs,
    get_commit_type,
    pretty_commit,
)


ON_PYTHON3 = (sys.version_info >= (3, 0))


def _needs_git(func):
    """
    Small decorator to make sure we have the git repo, or report error
    otherwise.
    """

    @wraps(func)
    def myfunc(*args, **kwargs):
        if not WITH_GIT:
            raise RuntimeError(
                "Dulwich library not available, can't extract info from the "
                "git repos."
            )
        return func(*args, **kwargs)

    return myfunc


@_needs_git
def get_changelog(repo_path, from_commit=None, bugtracker_url='',
                  rpm_format=False):
    """
    Given a repo path and an option commit/tag/refspec to start from, will
    get the rpm compatible changelog

    Args:
        repo_path (str): path to the git repo
        from_commit (str): refspec (partial commit hash, tag, branch, full
            refspec, partial refspec) to start the changelog from
        rpm_format(bool): if set, the changelog will be suitable to be uses as
            rpm package changelog.

    Returns:
        str: Rpm compatible changelog
    """
    repo = dulwich.repo.Repo(repo_path)
    tags = get_tags(repo)
    refs = get_refs(repo)
    changelog = []
    maj_version = 0
    feat_version = 0
    fix_version = 0
    start_including = False

    cur_line = ''
    if from_commit is None:
        start_including = True

    prev_version = (maj_version, feat_version, fix_version)

    for commit_sha, children in reversed(
        get_children_per_first_parent(repo_path).items()
    ):
        commit = get_repo_object(repo, commit_sha)
        maj_version, feat_version, fix_version = get_version(
            commit=commit,
            tags=tags,
            maj_version=maj_version,
            feat_version=feat_version,
            fix_version=fix_version,
            children=children,
        )
        version = (maj_version, feat_version, fix_version)
        version_str = '%s.%s.%s' % version

        if (
            start_including or commit_sha.startswith(from_commit) or
            fuzzy_matches_refs(from_commit, refs.get(commit_sha, []))
        ):
            commit_type = get_commit_type(
                commit=commit,
                children=children,
                tags=tags,
                prev_version=prev_version,
            )
            cur_line = pretty_commit(
                commit=commit,
                version=version_str,
                commit_type=commit_type,
                bugtracker_url=bugtracker_url,
                rpm_format=rpm_format,
            )
            for child in children:
                commit_type = get_commit_type(
                    commit=commit,
                    tags=tags,
                    prev_version=prev_version,
                )
                cur_line += pretty_commit(
                    commit=child,
                    version=None,
                    commit_type=commit_type,
                    bugtracker_url=bugtracker_url,
                )
            start_including = True
            changelog.append(cur_line)

        prev_version = version

    return '\n'.join(reversed(changelog))


@_needs_git
def get_current_version(repo_path):
    """
    Given a repo will return the version string, according to semantic
    versioning, counting as non-backwards compatible commit any one with a
    message header that matches (case insensitive)::

        sem-ver: .*break.*

    And as features any commit with a header matching::

        sem-ver: feature

    And counting any other as a bugfix

    Args:
        repo_path(str): path to the git repository to get the version for.

    Returns:
        str: Version string for that repository.
    """
    repo = dulwich.repo.Repo(repo_path)
    tags = get_tags(repo)
    maj_version = 0
    feat_version = 0
    fix_version = 0

    for commit_sha, children in reversed(
            list(get_children_per_first_parent(repo_path).items())
    ):
        commit = get_repo_object(repo, commit_sha)
        maj_version, feat_version, fix_version = get_version(
            commit=commit,
            tags=tags,
            maj_version=maj_version,
            feat_version=feat_version,
            fix_version=fix_version,
            children=children,
        )

    return '%s.%s.%s' % (maj_version, feat_version, fix_version)


@_needs_git
def tag_versions(repo_path):
    """
    Given a repo will add a tag for each major version.

    Args:
        repo_path(str): path to the git repository to tag.
    """
    repo = dulwich.repo.Repo(repo_path)
    tags = get_tags(repo)
    maj_version = 0
    feat_version = 0
    fix_version = 0
    last_maj_version = 0
    last_feat_version = 0
    result = []

    for commit_sha, children in reversed(
            get_children_per_first_parent(repo_path).items()
    ):
        commit = get_repo_object(repo, commit_sha)
        maj_version, feat_version, fix_version = get_version(
            commit=commit,
            tags=tags,
            maj_version=maj_version,
            feat_version=feat_version,
            fix_version=fix_version,
            children=children,
        )
        if (
            last_maj_version != maj_version or
            last_feat_version != feat_version
        ):
            last_maj_version = maj_version
            last_feat_version = feat_version
            tag_name = 'refs/tags/v%d.%d' % (maj_version, feat_version)
            if ON_PYTHON3:
                repo[str.encode(tag_name)] = commit
            else:
                repo[tag_name] = commit

            result.append(
                'v%d.%d -> %s' % (maj_version, feat_version, commit_sha)
            )

    return '\n'.join(result)


@_needs_git
def get_authors(repo_path, from_commit=None):
    """
    Given a repo and optionally a base revision to start from, will return
    the list of authors.

    Args:
        repo_path(str): Path to the code git repository.
        from_commit(str): Refspec of the commit to start aggregating the
            authors from.

    Returns:
        list: lexicographically sorted list of authors of the repo.
    """
    repo = dulwich.repo.Repo(repo_path)
    refs = get_refs(repo)
    start_including = False
    authors = set()

    if from_commit is None:
        start_including = True

    for commit_sha, children in reversed(
        get_children_per_first_parent(repo_path).items()
    ):
        commit = get_repo_object(repo, commit_sha)
        if (
            start_including or commit_sha.startswith(from_commit) or
            fuzzy_matches_refs(from_commit, refs.get(commit_sha, []))
        ):
            authors.add(_to_str(commit.author))
            for child in children:
                authors.add(_to_str(child.author))

            start_including = True

    return sorted(authors)


@_needs_git
def get_releasenotes(repo_path, from_commit=None, bugtracker_url=''):
    """
    Given a repo and optionally a base revision to start from, will return
    a text suitable for the relase notes announcement, grouping the bugs, the
    features and the api-breaking changes.

    Args:
        repo_path(str): Path to the code git repository.
        from_commit(str): Refspec of the commit to start aggregating the
            authors from.
        bugtracker_url(str): URL to be prepended to any bug ids found in the
            commits.

    Returns:
        str: Release notes text.
    """
    repo = dulwich.repo.Repo(repo_path)
    tags = get_tags(repo)
    refs = get_refs(repo)
    maj_version = 0
    feat_version = 0
    fix_version = 0
    start_including = False
    release_notes_per_major = OrderedDict()

    cur_line = ''
    if from_commit is None:
        start_including = True

    prev_version = (maj_version, feat_version, fix_version)
    prev_version_str = '%s.%s.%s' % prev_version
    bugs = []
    features = []
    api_break_changes = []

    for commit_sha, children in reversed(
        get_children_per_first_parent(repo_path).items()
    ):
        commit = get_repo_object(repo, commit_sha)
        maj_version, feat_version, fix_version = get_version(
            commit=commit,
            tags=tags,
            maj_version=maj_version,
            feat_version=feat_version,
            fix_version=fix_version,
            children=children,
        )
        version = (maj_version, feat_version, fix_version)
        version_str = '%s.%s.%s' % version

        if (
            start_including or commit_sha.startswith(from_commit) or
            fuzzy_matches_refs(from_commit, refs.get(commit_sha, []))
        ):
            start_including = True

            parent_commit_type = get_commit_type(
                commit=commit,
                children=children,
                tags=tags,
                prev_version=prev_version,
            )
            cur_line = pretty_commit(
                commit=commit,
                version=version_str,
                bugtracker_url=bugtracker_url,
                commit_type=parent_commit_type,
            )
            for child in children:
                commit_type = get_commit_type(
                    commit=commit,
                    tags=tags,
                    prev_version=prev_version,
                )
                cur_line += pretty_commit(
                    commit=child,
                    version=None,
                    commit_type=commit_type,
                    bugtracker_url=bugtracker_url,
                )

            if parent_commit_type == 'api_break':
                release_notes_per_major[prev_version_str] = (
                    api_break_changes,
                    features,
                    bugs,
                )
                bugs, features, api_break_changes = [], [], []
                api_break_changes.append(cur_line)
            elif parent_commit_type == 'feature':
                features.append(cur_line)
            else:
                bugs.append(cur_line)

        prev_version = version
        prev_version_str = version_str

    release_notes_per_major[prev_version_str] = (
        api_break_changes,
        features,
        bugs,
    )

    releasenotes = ''
    for major_version, lines in reversed(release_notes_per_major.items()):
        api_break_changes, features, bugs = lines
        releasenotes += u'''New changes for version %s
=================================

API Breaking changes
--------------------
%s
New features
------------
%s
Bugfixes and minor changes
--------------------------
%s

''' % (
                major_version,
                (
                    '\n'.join(reversed(api_break_changes)) or
                    'No new API breaking changes\n'
                ),
                '\n'.join(reversed(features)) or 'No new features\n',
                '\n'.join(reversed(bugs)) or 'No new bugs\n',
            )

    return releasenotes.strip()
