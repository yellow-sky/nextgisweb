# -*- coding: utf-8 -*-
from pyramid.security import authenticated_userid
from sqlalchemy.orm.exc import NoResultFound

from ..component import Component


@Component.registry.register
class AuthComponent(Component):
    identity = 'auth'

    def initialize_db(self):
        self.initialize_user(
            system=True,
            keyname='guest',
            display_name=u"Гость"
        )

        self.initialize_user(
            system=True,
            keyname='everyone',
            display_name=u"Любой пользователь"
        ).persist()

        self.initialize_user(
            system=True,
            keyname='authenticated',
            display_name=u"Прошедший проверку"
        ).persist()

        self.initialize_group(
            keyname='administrators',
            display_name=u"Администраторы",
            members=[self.initialize_user(
                keyname='administrator',
                display_name=u"Администратор"
            ), ]
        ).persist()

        self.initialize_user(
            keyname="ivanov",
            display_name=u"Иванов А.А."
        )

        self.initialize_user(
            keyname="petrov",
            display_name=u"Петров Б.Б."
        )

        self.initialize_user(
            keyname="sidorov",
            display_name=u"Сидоров В.В."
        )

    def initialize(self):
        from . import models
        models.initialize(self)

    def setup_pyramid(self, config):

        def user(request):
            user_id = authenticated_userid(request)
            if user_id:
                return self.User.filter_by(id=user_id).one()
            else:
                return self.User.filter_by(keyname='guest').one()

        config.set_request_property(user, 'user', reify=True)

        from . import views
        views.setup_pyramid(self, config)

    def initialize_user(self, keyname, **kwargs):
        """ Проверяет наличие в БД пользователя с keyname и в случае
        отсутствия создает его с параметрами kwargs """

        try:
            obj = self.User.filter_by(keyname=keyname).one()
        except NoResultFound:
            obj = self.User(keyname=keyname, **kwargs).persist()

        return obj

    def initialize_group(self, keyname, **kwargs):
        """ Проверяет наличие в БД группы пользователей с keyname и в случае
        отсутствия создает ее с параметрами kwargs """

        try:
            obj = self.Group.filter_by(keyname=keyname).one()
        except NoResultFound:
            obj = self.Group(keyname=keyname, **kwargs).persist()

        return obj
