import factory


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user%d@food.net' % n)

    class Meta:
        model = 'auth.User'


class UserProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'membership.UserProfile'


class AccountFactory(factory.DjangoModelFactory):
    number = factory.Sequence(lambda n: '%d' % n)
    department = factory.SubFactory(
        'foodnet.membership.factories.DepartmentFactory'
    )
    category = factory.SubFactory(
        'foodnet.membership.factories.AccountCategoryFactory'
    )

    class Meta:
        model = 'membership.Account'


class AccountCategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'membership.AccountCategory'


class AccountMembershipFactory(factory.DjangoModelFactory):
    user_profile = factory.SubFactory('foodnet.membership.factories.UserProfileFactory')
    account = factory.SubFactory('foodnet.membership.factories.AccountFactory')

    class Meta:
        model = 'membership.AccountMembership'


class DepartmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'membership.Department'


class DepartmentAdministratorFactory(factory.DjangoModelFactory):
    admin = factory.SubFactory('foodnet.membership.factories.UserProfileFactory')
    department = factory.SubFactory('foodnet.membership.factories.DepartmentFactory')

    class Meta:
        model = 'membership.DepartmentAdministrator'


class DepartmentInvitationFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'membership.DepartmentInvitation'
