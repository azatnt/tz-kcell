from django.contrib.auth.models import User
from django.db.models import Prefetch

from main.models import Contact
from main.serializers import UserSerializer, UserWithContactSerializer, ContactWithUserSerializer, \
    ContactGroupedByUserSerializer


def check_and_create_contact(user: User, contacts: dict) -> bool:
    "Checks if contact exists, if not then create"
    does_exist = False
    if not Contact.objects.filter(**contacts).exists():
        Contact.objects.create(user=user, **contacts)
        does_exist = True
    return does_exist


def get_contact_by_user(user_id: int) -> User:
    "Returns all contacts of one exact user"
    user = User.objects.filter(id=user_id).prefetch_related(Prefetch('user_contact', Contact.objects.all()))
    if user.exists():
        result = UserWithContactSerializer(user.first()).data
        return result
    return None


def get_all_contacts_grouped_by_user() -> User:
    "Return all contacts grouped by users"
    users = User.objects.all().prefetch_related(Prefetch('user_contact', Contact.objects.all()))
    result = ContactGroupedByUserSerializer(users, many=True).data
    return result


def get_all_users_and_contacts() -> User:
    "Return all contacts of all users"
    contacts = Contact.objects.all().select_related('user')
    result = ContactWithUserSerializer(contacts, many=True).data
    return result
