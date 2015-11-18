# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SciFabric LTD.
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.


class ResultAuth(object):
    _specific_actions = []

    def __init__(self, project_repo):
        self.project_repo = project_repo

    @property
    def specific_actions(self):
        return self._specific_actions

    def can(self, user, action, result=None, project_id=None):
        action = ''.join(['_', action])
        return getattr(self, action)(user, result, project_id)

    def _create(self, user, result, project_id=None):
        return False

    def _read(self, user, result=None, project_id=None):
        if (result is None and project_id is None):
            return False
        return True

    def _update(self, user, result, project_id=None):
        if user.is_anonymous():
            return False
        project = self._get_project(result, result.project_id)
        return ((project.owner_id == user.id) and
                (result.project_id == project_id))

    def _delete(self, user, result, project_id=None):
        return False

    def _get_project(self, result, project_id):
        if result is not None:
            return self.project_repo.get(result.project_id)
        return self.project_repo.get(project_id)
