from django.test import TestCase
from django.contrib.auth import get_user_model
from userdb.models import Region

User = get_user_model()


class RegionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Region.objects.create(name="bham", description="University of Birmingham")

    def test_object_str_is_name(self):
        region = Region.objects.all().first()
        print(User.objects.all())
        self.assertEqual(str(region), region.name)
