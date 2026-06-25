from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from peethas.models import Peetha, Pooja, PoojaBooking, PeethaPaymentConfig, FeatureFlag, PeethaHandler
import datetime

class PoojaBookingTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testdevotee', password='password123')
        
        # Create Peetha
        self.peetha = Peetha.objects.create(
            name='Kashi Peetha',
            slug='kashi',
            acharya='Jagadguru',
            simhasana='Ganga Simhasana',
            location='Varanasi',
            color='#FF9900'
        )
        
        # Create Payment Config (required for initiate_pooja_booking)
        self.payment_config = PeethaPaymentConfig.objects.create(
            peetha=self.peetha,
            razorpay_key_id='rzp_test_123',
            razorpay_key_secret='secret_123',
            is_active=True
        )

        # Create Pooja (Available Mon, Wed, Fri only; 2 slots max)
        self.pooja = Pooja.objects.create(
            peetha=self.peetha,
            name='Special Kashi Pooja',
            price=500.00,
            total_slots=2,
            available_days='Monday,Wednesday,Friday',
            is_active=True
        )
        
        # Client
        self.client = Client()
        self.client.login(username='testdevotee', password='password123')

    def test_booking_past_date_fails(self):
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Devotee',
                'devotee_phone': '1234567890',
                'date_of_pooja': yesterday
            }
        )
        self.assertEqual(response.status_code, 302)
        # Check that no booking was created
        self.assertEqual(PoojaBooking.objects.count(), 0)

    def test_booking_invalid_weekday_fails(self):
        # Find next Tuesday
        today = datetime.date.today()
        days_ahead = (1 - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        next_tuesday = (today + datetime.timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        response = self.client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Devotee',
                'devotee_phone': '1234567890',
                'date_of_pooja': next_tuesday
            }
        )
        self.assertEqual(response.status_code, 302)
        # Check that no booking was created
        self.assertEqual(PoojaBooking.objects.count(), 0)

    def test_booking_slots_limit(self):
        # Find next Monday
        today = datetime.date.today()
        days_ahead = (0 - today.weekday()) % 7
        next_monday = today + datetime.timedelta(days=days_ahead)
        next_monday_str = next_monday.strftime('%Y-%m-%d')
        
        # First booking
        response = self.client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Devotee 1',
                'devotee_phone': '1234567890',
                'date_of_pooja': next_monday_str
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PoojaBooking.objects.count(), 1)
        
        # Second booking
        response = self.client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Devotee 2',
                'devotee_phone': '1234567890',
                'date_of_pooja': next_monday_str
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PoojaBooking.objects.count(), 2)
        
        # Third booking - slots full, should redirect with error
        response = self.client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Devotee 3',
                'devotee_phone': '1234567890',
                'date_of_pooja': next_monday_str
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PoojaBooking.objects.count(), 2)

    def test_pooja_availability_api(self):
        # Create one booking for next Monday
        today = datetime.date.today()
        days_ahead = (0 - today.weekday()) % 7
        next_monday = today + datetime.timedelta(days=days_ahead)
        next_monday_str = next_monday.strftime('%Y-%m-%d')
        
        days_ahead_tue = (1 - today.weekday()) % 7
        if days_ahead_tue == 0:
            days_ahead_tue = 7
        next_tuesday_str = (today + datetime.timedelta(days=days_ahead_tue)).strftime('%Y-%m-%d')

        PoojaBooking.objects.create(
            pooja=self.pooja,
            devotee_name='Test Devotee',
            devotee_phone='1234567890',
            date_of_pooja=next_monday,
            amount=self.pooja.price,
            payment_status='success'
        )

        response = self.client.get(
            reverse('peethas:pooja_availability', kwargs={
                'peetha_slug': self.peetha.slug,
                'pooja_id': self.pooja.id
            }),
            {'year': next_monday.year, 'month': next_monday.month}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('availability', data)
        self.assertEqual(data['availability'][next_monday_str], 'fast')
        self.assertEqual(data['availability'][next_tuesday_str], 'not_open')

    def test_profile_view_flow(self):
        # 1. Test GET request to profile view
        response = self.client.get(reverse('peethas:profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile Completion")

        # 2. Test POST request to update profile
        response = self.client.post(
            reverse('peethas:profile_view'),
            {
                'first_name': 'Updated Devotee Name',
                'email': 'updated@example.com',
                'phone_number': '9876543210',
                'address': '123 Temple Road',
                'gender': 'female',
                'gotra': 'Kashyapa',
                'nakshatra': 'Aswini',
                'rashi': 'Mesha'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify database was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated Devotee Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        
        profile = self.user.profile
        self.assertEqual(profile.phone_number, '9876543210')
        self.assertEqual(profile.address, '123 Temple Road')
        self.assertEqual(profile.gender, 'female')
        self.assertEqual(profile.gotra, 'Kashyapa')
        self.assertEqual(profile.nakshatra, 'Aswini')
        self.assertEqual(profile.rashi, 'Mesha')
        self.assertEqual(profile.completion_percentage(), 88)

    def test_pooja_booking_disabled_flag(self):
        # Create and disable kashi_pooja_booking
        flag, _ = FeatureFlag.objects.get_or_create(name='kashi_pooja_booking')
        flag.is_enabled = False
        flag.save()
        
        # 1. Attempt to fetch availability - should return 403
        response = self.client.get(
            reverse('peethas:pooja_availability', kwargs={
                'peetha_slug': self.peetha.slug,
                'pooja_id': self.pooja.id
            })
        )
        self.assertEqual(response.status_code, 403)
        
        # 2. Attempt to initiate pooja booking - should redirect (302)
        response = self.client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Test Devotee',
                'devotee_phone': '1234567890',
                'date_of_pooja': '2026-07-01'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_overall_disabled_flag_disables_pooja_booking(self):
        # Disable kashi_overall
        flag, _ = FeatureFlag.objects.get_or_create(name='kashi_overall')
        flag.is_enabled = False
        flag.save()
        
        # 1. Attempt to fetch availability - should return 403
        response = self.client.get(
            reverse('peethas:pooja_availability', kwargs={
                'peetha_slug': self.peetha.slug,
                'pooja_id': self.pooja.id
            })
        )
        self.assertEqual(response.status_code, 403)
        
        # 2. Attempt to initiate pooja booking - should redirect (302)
        response = self.client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Test Devotee',
                'devotee_phone': '1234567890',
                'date_of_pooja': '2026-07-01'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_feature_flag_cascading_logic(self):
        admin_user = User.objects.create_superuser(username='adminuser', password='password123', email='admin@example.com')
        admin_client = Client()
        admin_client.login(username='adminuser', password='password123')
        
        overall_flag, _ = FeatureFlag.objects.get_or_create(name='kashi_overall', defaults={'is_enabled': True})
        pooja_flag, _ = FeatureFlag.objects.get_or_create(name='kashi_pooja_booking', defaults={'is_enabled': True})
        acc_flag, _ = FeatureFlag.objects.get_or_create(name='kashi_accommodation', defaults={'is_enabled': True})
        
        overall_flag.is_enabled = True
        overall_flag.save()
        pooja_flag.is_enabled = True
        pooja_flag.save()
        acc_flag.is_enabled = True
        acc_flag.save()
        
        response = admin_client.post(
            reverse('peethas:toggle_feature', kwargs={'pk': overall_flag.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        overall_flag.refresh_from_db()
        pooja_flag.refresh_from_db()
        acc_flag.refresh_from_db()
        self.assertFalse(overall_flag.is_enabled)
        self.assertFalse(pooja_flag.is_enabled)
        self.assertFalse(acc_flag.is_enabled)
        
        overall_flag.is_enabled = False
        overall_flag.save()
        pooja_flag.is_enabled = False
        pooja_flag.save()
        acc_flag.is_enabled = False
        acc_flag.save()
        
        response = admin_client.post(
            reverse('peethas:toggle_feature', kwargs={'pk': pooja_flag.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        overall_flag.refresh_from_db()
        pooja_flag.refresh_from_db()
        acc_flag.refresh_from_db()
        self.assertTrue(overall_flag.is_enabled)
        self.assertTrue(pooja_flag.is_enabled)
        self.assertFalse(acc_flag.is_enabled)

    def test_assign_user_roles(self):
        admin_user = User.objects.create_superuser(username='roleadmin', password='password123', email='roleadmin@example.com')
        admin_client = Client()
        admin_client.login(username='roleadmin', password='password123')
        
        # Create a standard user to manipulate
        test_user = User.objects.create_user(username='test_devotee_role', password='password123', email='test_devotee_role@example.com')
        
        # 1. Assign Staff Role
        response = admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'assign',
                'user': test_user.id,
                'role': 'staff'
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_staff)
        self.assertFalse(PeethaHandler.objects.filter(user=test_user).exists())
        
        # 2. Assign Handler Role (should revoke staff, map handler)
        response = admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'assign',
                'user': test_user.id,
                'role': 'handler',
                'peetha': self.peetha.id
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertFalse(test_user.is_staff)
        self.assertTrue(PeethaHandler.objects.filter(user=test_user, peetha=self.peetha).exists())
        
        # 3. Revoke Handler Role
        handler = PeethaHandler.objects.get(user=test_user)
        response = admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'delete',
                'handler_id': handler.id
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertFalse(test_user.is_staff)
        self.assertFalse(PeethaHandler.objects.filter(user=test_user).exists())
        
        # 4. Assign Staff Role again, then revoke staff
        admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'assign',
                'user': test_user.id,
                'role': 'staff'
            }
        )
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_staff)
        
        response = admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'revoke_staff',
                'user_id': test_user.id
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

        # 5. Assign Super Admin Role
        response = admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'assign',
                'user': test_user.id,
                'role': 'superuser'
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_staff)
        self.assertTrue(test_user.is_superuser)

        # 6. Revoke Super Admin Access (revoke_staff should demote superuser)
        response = admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'revoke_staff',
                'user_id': test_user.id
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

        # 7. Assign Super Admin and then change to Devotee role
        admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'assign',
                'user': test_user.id,
                'role': 'superuser'
            }
        )
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_superuser)

        response = admin_client.post(
            reverse('peethas:assign_handler'),
            {
                'action': 'assign',
                'user': test_user.id,
                'role': 'devotee'
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    def test_devotee_search_excludes_non_devotees(self):
        admin_user = User.objects.create_superuser(username='searchadmin', password='password123', email='searchadmin@example.com')
        admin_client = Client()
        admin_client.login(username='searchadmin', password='password123')
        
        # 1. Devotee user (should be included in devotee search results)
        devotee_user = User.objects.create_user(username='true_devotee', password='password123')
        
        # 2. Staff user (should be excluded)
        staff_user = User.objects.create_user(username='staff_user_role', password='password123', is_staff=True)
        
        # 3. Handler user (should be excluded)
        handler_user = User.objects.create_user(username='handler_user_role', password='password123')
        PeethaHandler.objects.create(user=handler_user, peetha=self.peetha)
        
        # 4. Superuser (should be excluded)
        superuser_user = User.objects.create_superuser(username='super_user_role', password='password123', email='super_user_role@example.com')
        
        response = admin_client.get(reverse('peethas:dashboard_search_devotees'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        usernames = [d['username'] for d in data['devotees']]
        
        self.assertIn('true_devotee', usernames)
        self.assertNotIn('staff_user_role', usernames)
        self.assertNotIn('handler_user_role', usernames)
        self.assertNotIn('super_user_role', usernames)



