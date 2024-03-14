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

"""
Script to generate the version, changelog and releasenotes from the git
repository.
"""
from __future__ import print_function

import datetime
import os
import re
from collections import OrderedDict, defaultdict

import dulwich.repo
import dulwich.walk

BUG_URL_REG = re.compile(
    r'.*(closes #|fixes #|adresses #)(?P<bugid>\d+)'
)
VALID_TAG = re.compile(r'^v?\d+\.\d+(\.\d+)?$')
FEAT_HEADER = re.compile(
    r'\nsem-ver:\s*.*(feature|deprecat).*(\n|$)',
    flags=re.IGNORECASE,
)
FEAT_MSG = re.compile(r'\n\* NEW')
MAJOR_HEADER = re.compile(r'\nsem-ver:\s*.*break.*(\n|$)', flags=re.IGNORECASE)
MAJOR_MSG = re.compile(r'\n\* INCOMPATIBLE')


def _to_str(maybe_str):
    # python3 support magic
    try:
        assert isinstance(u'', str)
        unicode = type(None)
    except AssertionError:
        unicode = type(u'')

    if isinstance(maybe_str, unicode):
        maybe_str = maybe_str.encode('utf-8')

    else:
        try:
            maybe_str = maybe_str.decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
            pass

    return maybe_str


def _tag2tuple(tag):
    feat_version = 0
    fix_version = 0
    version = tag.split('.')
    if len(version) == 1:
        maj_version = version[0]
    if len(version) == 2:
        maj_version, feat_version = version
    if len(version) == 3:
        maj_version, feat_version, fix_version = version

    if maj_version.startswith('v'):
        maj_version = maj_version[1:]

    maj_version = int(maj_version)
    feat_version = int(feat_version)
    fix_version = int(fix_version)

    return maj_version, feat_version, fix_version


def get_repo_object(repo, object_name):
    try:
        object_name = object_name.encode()
    except:
        pass

    return repo.get_object(object_name)


def split_line(what, indent='', cols=79):
    """Split a line on the closest space, or break the last word with '-'.

    Args:
        what(str): text to spli one line of.
        indent(str): will prepend this indent to the split line, taking it into
        account in the column count.
        cols(int): maximum length of the split line.

    Returns:
        tuple(str, str): rest of the text and split line in that order.

    Raises:
        ValueError: when the indent is greater than the indent, or the cols
        param is too small
    """
    if len(indent) > cols:
        raise ValueError("The indent can't be longer than cols.")

    if cols < 2:
        raise ValueError(
            "The cols can't be smaller than 2 (a char plus a possible '-')"
        )

    what = indent + what.lstrip()

    if len(what) <= cols:
        what, new_line = '', what
    else:
        try:
            closest_space = what[:cols].rindex(' ')
        except ValueError:
            closest_space = -1

        if closest_space > len(indent):
            what, new_line = (
                what[closest_space:],
                what[:closest_space],
            )
        elif what[cols] == ' ':
            what, new_line = (
                what[cols:],
                what[:cols],
            )
        else:
            what, new_line = what[cols - 1:], what[:cols - 1] + '-'

    return what.lstrip(), new_line.rstrip()


def fit_to_cols(what, indent='', cols=79):
    """Wrap the given text to the columns, prepending the indent to each line.

    Args:
        what(str): text to wrap.
        indent(str): indentation to use.
        cols(int): colt to wrap to.

    Returns:
        str: Wrapped text
    """
    lines = []
    while what:
        what, next_line = split_line(
            what=what,
            cols=cols,
            indent=indent,
        )
        lines.append(next_line)

    return '\n'.join(lines)


def get_bugs_from_commit_msg(commit_msg):
    bugs = []
    for line in _to_str(commit_msg).split('\n'):
        match = BUG_URL_REG.match(_to_str(line))
        if match:
            bugs.append(match.groupdict()['bugid'])
    return bugs


def pretty_commit(commit, version=None, commit_type='bug', bugtracker_url='',
                  rpm_format=False):
    message = _to_str(commit.message)
    subject = _to_str(commit.message).split('\n', 1)[0]  # noqa
    short_hash = commit.sha().hexdigest()[:8]  # noqa
    author = _to_str(commit.author)  # noqa
    author_date = datetime.datetime.fromtimestamp(  # noqa
            int(commit.commit_time)
    ).strftime('%a %b %d %Y')
    bugs = get_bugs_from_commit_msg(commit.message)
    if bugs:
        changelog_bugs = fit_to_cols(
            'FIXED ISSUES: ' + ', '.join(
                '{bugtracker_url}{bug}'.format(
                    bugtracker_url=bugtracker_url,
                    bug=bug,
                ) for bug in bugs
            ),
            indent='    ',
        ) + '\n'
    else:
        changelog_bugs = ''  # noqa

    feature_header = ''
    if commit_type == 'feature':
        feature_header = 'FEATURE'
    elif commit_type == 'api_break':
        feature_header = 'MAJOR'
    else:
        feature_header = 'MINOR'

    changelog_message = fit_to_cols(  # noqa
        u'{feature_header} {short_hash}: {subject}'.format(**vars()),
        indent='    ',
    )

    if rpm_format:
        return (
            (
                u'* {author_date} {author} - {version}\n'
                if version is not None else ''
            ) + '{changelog_message}\n' + '{changelog_bugs}'
        ).format(**vars())

    return (
        (
            u'* {version} "{author}"\n'
            if version is not None else ''
        ) + '{changelog_message}\n' + '{changelog_bugs}'
    ).format(**vars())


def get_tags(repo):
    tags = {}
    for tag_ref, commit in repo.get_refs().items():
        tag_ref = _to_str(tag_ref)
        if tag_ref.startswith('refs/tags/') and VALID_TAG.match(
            tag_ref[len('refs/tags/'):]
        ):
            tags[_to_str(commit)] = os.path.basename(tag_ref)

    return tags


def get_refs(repo):
    refs = defaultdict(set)
    for ref, commit in repo.get_refs().items():
        refs[commit].add(commit)
        refs[commit].add(ref)
    return refs


def fuzzy_matches_ref(fuzzy_ref, ref):
    cur_section = ''
    for path_section in reversed(_to_str(ref).split('/')):
        cur_section = os.path.normpath(os.path.join(path_section, cur_section))
        if fuzzy_ref == cur_section:
            return True
    return False


def fuzzy_matches_refs(fuzzy_ref, refs):
    return any(fuzzy_matches_ref(fuzzy_ref, ref) for ref in refs)


def get_children_per_parent(repo_path):
    repo = dulwich.repo.Repo(repo_path)
    children_per_parent = defaultdict(set)

    for entry in repo.get_walker(order=dulwich.walk.ORDER_TOPO):
        for parent in entry.commit.parents:
            children_per_parent[_to_str(parent)].add(
                entry.commit.sha().hexdigest()
            )

    return children_per_parent


def get_first_parents(repo_path):
    repo = dulwich.repo.Repo(repo_path)
    #: these are the commits that are parents of more than one other commit
    first_parents = []
    on_merge = False

    for entry in repo.get_walker(order=dulwich.walk.ORDER_TOPO):
        commit = entry.commit
        # In order to properly work on python 2 and 3 we need some utf magic
        parents = commit.parents and [_to_str(i) for i in commit.parents]
        if not parents:
            if commit.sha().hexdigest() not in first_parents:
                first_parents.append(commit.sha().hexdigest())
        elif len(parents) == 1 and not on_merge:
            if commit.sha().hexdigest() not in first_parents:
                first_parents.append(commit.sha().hexdigest())
            if parents[0] not in first_parents:
                first_parents.append(parents[0])
        elif len(parents) > 1 and not on_merge:
            on_merge = True
            if commit.sha().hexdigest() not in first_parents:
                first_parents.append(commit.sha().hexdigest())
            if parents[0] not in first_parents:
                first_parents.append(parents[0])
        elif parents and commit.sha().hexdigest() in first_parents:
            if parents[0] not in first_parents:
                first_parents.append(parents[0])

    return first_parents


def has_firstparent_child(sha, first_parents, parents_per_child):
    return any(
        child for child in parents_per_child[sha] if child in first_parents
    )


def get_merged_commits(repo, commit, first_parents, children_per_parent):
    merge_children = set()

    to_explore = set([commit.sha().hexdigest()])

    while to_explore:
        next_sha = to_explore.pop()
        try:
            next_commit = get_repo_object(repo, next_sha)
        except KeyError:
            continue

        if (
            next_sha not in first_parents and not has_firstparent_child(
                next_sha, first_parents, children_per_parent
            ) or next_sha.encode('utf-8') in commit.parents
        ):
            merge_children.add(next_sha)

        non_first_parents = (
            parent
            for parent in next_commit.parents
            if _to_str(parent) not in first_parents
        )
        for child_sha in non_first_parents:
            if child_sha not in merge_children and child_sha != next_sha:
                to_explore.add(child_sha)

    return merge_children


def get_children_per_first_parent(repo_path):
    repo = dulwich.repo.Repo(repo_path)
    first_parents = get_first_parents(repo_path)
    children_per_parent = get_children_per_parent(repo_path)
    children_per_first_parent = OrderedDict()

    for first_parent in first_parents:
        try:
            commit = get_repo_object(repo, first_parent)
        except KeyError:
            continue

        if len(commit.parents) > 1:
            children = get_merged_commits(
                repo=repo,
                commit=commit,
                first_parents=first_parents,
                children_per_parent=children_per_parent,
            )
        else:
            children = set()

        children_per_first_parent[first_parent] = [
            get_repo_object(repo, child) for child in children
        ]

    return children_per_first_parent


def get_version(commit, tags, maj_version=0, feat_version=0, fix_version=0,
                children=None):
    children = children or []
    commit_type = get_commit_type(commit, children)
    commit_sha = commit.sha().hexdigest()

    if commit_sha in tags:
        maj_version, feat_version, fix_version = _tag2tuple(tags[commit_sha])
    elif commit_type == 'api_break':
        maj_version += 1
        feat_version = 0
        fix_version = 0
    elif commit_type == 'feature':
        feat_version += 1
        fix_version = 0
    else:
        fix_version += 1

    version = (maj_version, feat_version, fix_version)
    return version


def is_api_break(commit):
    return bool(
        MAJOR_HEADER.search(_to_str(commit.message)) or
        MAJOR_MSG.search(_to_str(commit.message))
    )


def is_feature(commit):
    return bool(
        FEAT_HEADER.search(_to_str(commit.message)) or
        FEAT_MSG.search(_to_str(commit.message))
    )


def get_commit_type(commit, children=None, tags=None, prev_version=None):
    children = children or []
    tags = tags or []
    prev_version = prev_version or (0, 0, 0)
    commit_sha = commit.sha().hexdigest()

    if commit_sha in tags:
        maj_version, feat_version, _ = _tag2tuple(tags[commit_sha])
        if maj_version > prev_version[0]:
            return 'api_break'
        elif feat_version > prev_version[1]:
            return 'feature'
        return 'bug'

    if any(is_api_break(child) for child in children + [commit]):
        return 'api_break'
    elif any(is_feature(child) for child in children + [commit]):
        return 'feature'
    else:
        return 'bug'
