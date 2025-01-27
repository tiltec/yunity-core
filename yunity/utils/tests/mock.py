from factory import DjangoModelFactory, CREATE_STRATEGY, LazyAttribute, post_generation, SubFactory, PostGeneration

from yunity.models import Category
from yunity.utils.tests.fake import faker


class Mock(DjangoModelFactory):
    class Meta:
        strategy = CREATE_STRATEGY
        model = None
        abstract = True


class MockCategory(Mock):
    class Meta:
        model = "yunity.Category"
        strategy = CREATE_STRATEGY

    name = LazyAttribute(lambda _: ' '.join(faker.words(5)))
    parent = None


class MockUser(Mock):
    class Meta:
        model = "yunity.User"
        strategy = CREATE_STRATEGY

    is_active = True
    is_staff = False
    type = Category.objects.filter(name='user.default').first()
    display_name = LazyAttribute(lambda _: faker.name())
    email = LazyAttribute(lambda _: faker.email())
    password = PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.display_name))
    locations = LazyAttribute(lambda _: [faker.location() for _ in range(2)])


class MockChat(Mock):
    class Meta:
        model = "yunity.Chat"
        strategy = CREATE_STRATEGY

    administrated_by = SubFactory(MockUser)

    @post_generation
    def participants(self, created, participants, **kwargs):
        if not created:
            return
        if participants:
            for participant in participants:
                self.participants.add(participant)
