from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import TextField, ForeignKey, DateTimeField, OneToOneField, ManyToManyField, EmailField, \
    BooleanField
from django.utils import timezone

from yunity.models.abstract import MapItem, Conversation, Request
from yunity.elasticsearch.core import get_es_type
from yunity.utils.models.abc import BaseModel
from yunity.utils.models.field import MaxLengthCharField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, locations=None, category=None, display_name=None, **extra_fields):
        """ Creates and saves a User with the given username, email and password.

        """
        email = self._validate_email(email)

        user = self.model(
            email=email,
            is_active=True,
            locations=locations or {'latitude': 0.0, 'longitude': 0.0},
            type=category or Category.objects.get(name="user.default"),
            display_name=display_name or email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _validate_email(self, email):
        if email is None:
            raise ValueError('The given email must be set')
        return self.normalize_email(email)

    def create_user(self, email=None, password=None, locations=None, category=None, display_name=None, **extra_fields):
        return self._create_user(email, password, locations, category, display_name, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, None, None, None, **extra_fields)


class User(AbstractBaseUser, MapItem):
    email = EmailField(max_length=64, unique=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    date_joined = DateTimeField(default=timezone.now)
    display_name = TextField()
    picture_url = TextField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def to_es(self):
        return super().to_es()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class Valuable(MapItem):

    def get_es_type(self):
        category_name = self.type.name
        return get_es_type('valuable', category_name)


class Opportunity(MapItem):

    def get_es_type(self):
        category_name = self.type.name
        return get_es_type('opportunity', category_name)


class Category(BaseModel):
    parent = ForeignKey('self', null=True, related_name='children')

    name = MaxLengthCharField(unique=True)


class Message(BaseModel):
    sent_by = ForeignKey('yunity.User')
    reply_to = ForeignKey('self', null=True, related_name='replies')
    in_conversation = ForeignKey('yunity.Conversation', related_name='messages')

    created_at = DateTimeField(auto_now=True)
    type = MaxLengthCharField()
    content = TextField()


class Interaction(BaseModel):
    created_at = DateTimeField(auto_now=True)
    type = MaxLengthCharField()
    payload = TextField()

    caused_by = ForeignKey('yunity.User', related_name='interation_caused')
    changed = OneToOneField('yunity.VersionTrait')


class Feedback(BaseModel):
    about = OneToOneField('yunity.FeedbackTrait')
    provided_by = OneToOneField('yunity.User', related_name='feedback_provider')
    arbitrated_by = ManyToManyField('yunity.User', related_name='feedback_arbitrators')

    status = MaxLengthCharField()
    type = MaxLengthCharField()


class Chat(Conversation):
    participants = ManyToManyField('yunity.User')

    name = MaxLengthCharField(null=True)


class Wall(Conversation):
    target = OneToOneField('yunity.MapItem')


class ArbitrationLog(Conversation):
    target = OneToOneField('yunity.Feedback')


class Participate(Request):
    target = ForeignKey('yunity.Opportunity')

    type = MaxLengthCharField()


class Take(Request):
    target = ForeignKey('yunity.Valuable')
