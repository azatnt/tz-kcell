from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register_urls'),
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair_urls'),
    path('add-contact/', AddContact.as_view(), name='add_contact_urls'),
    path('get-contact-by-user/<int:id>/', GetContactByUser.as_view(), name='get_contact_by_user_urls'),
    path('get-all-contacts/', GetAllContacts.as_view(), name='get_all_contact_urls'),
    path('export_excel_contacts/', ExportExcelContacts.as_view(), name='export_excel_contacts_urls')
]
