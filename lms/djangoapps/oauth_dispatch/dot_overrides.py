"""
Classes that override default django-oauth-toolkit behavior
"""
from __future__ import unicode_literals

import time
from datetime import datetime
from pytz import utc

from django.contrib.auth import authenticate, get_user_model
from oauth2_provider.oauth2_validators import OAuth2Validator

from oauth2_provider.models import AccessToken
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


@receiver(pre_save, sender=AccessToken)
def on_access_token_presave(sender, instance, *args, **kwargs):
    """
    A hook on the AccessToken. For when we grant authorization-codes,
    since we do not have protected scopes, we must mark all
    AcessTokens as expired.

    We do this as a pre-save hook on the ORM
    """
    force_expire = (
        instance.application.authorization_grant_type == 'authorization-code' and
        getattr(settings, 'OAUTH2_PROVIDER', {}).get('AUTOEXPIRE_AUTHORIZATION_CODE_ACCESS_TOKENS', True)
    )

    if force_expire:
        # put the expire timestamp into the beginning of the epoch
        instance.expires = datetime(1970, 1, 1, tzinfo=utc)


class EdxOAuth2Validator(OAuth2Validator):
    """
    Validator class that implements edX-specific custom behavior:

        * It allows users to log in with their email or username.
        * It does not require users to be active before logging in.
    """

    def validate_user(self, username, password, client, request, *args, **kwargs):
        """
        Authenticate users, but allow inactive users (with u.is_active == False)
        to authenticate.
        """
        user = self._authenticate(username=username, password=password)
        if user is not None:
            request.user = user
            return True
        return False

    def _authenticate(self, username, password):
        """
        Authenticate the user, allowing the user to identify themself either by
        username or email
        """

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is None:
            UserModel = get_user_model()  # pylint: disable=invalid-name
            try:
                email_user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                authenticated_user = None
            else:
                authenticated_user = authenticate(username=email_user.username, password=password)
        return authenticated_user

    def save_bearer_token(self, token, request, *args, **kwargs):
        """
        Ensure that access tokens issued via client credentials grant are associated with the owner of the
        ``Application``.
        """
        grant_type = request.grant_type
        user = request.user

        if grant_type == 'client_credentials':
            # Temporarily remove the grant type to avoid triggering the super method's code that removes request.user.
            request.grant_type = None

            # Ensure the tokens get associated with the correct user since DOT does not normally
            # associate access tokens issued with the client_credentials grant to users.
            request.user = request.client.user

        super(EdxOAuth2Validator, self).save_bearer_token(token, request, *args, **kwargs)

        # costumized oauth2 provider behavior for Open edX
        force_expire = (
            request.client.authorization_grant_type == 'authorization-code' and
            getattr(settings, 'OAUTH2_PROVIDER', {}).get('AUTOEXPIRE_AUTHORIZATION_CODE_ACCESS_TOKENS', True)
        )
        if force_expire:
            # For now, since Open edX doesn't have the protection of scopes, any access token
            # that was generated through three-legged oauth schemes
            # must be automatically expired. So let's update
            # the token dictionary, so set the expires_in field be
            # on Jan. 1, 1970
            token['expires_in'] = -int(time.time())

        # Restore the original request attributes
        request.grant_type = grant_type
        request.user = user
