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
                'rashi': 'Mesha',
                'date_of_birth': '1990-05-15'
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
        self.assertEqual(profile.date_of_birth, datetime.date(1990, 5, 15))
        self.assertEqual(profile.completion_percentage(), 90)

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
                'role': 'staff',
                'peetha': self.peetha.id
            }
        )
        self.assertEqual(response.status_code, 302)
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_staff)
        self.assertTrue(PeethaHandler.objects.filter(user=test_user, peetha=self.peetha).exists())
        
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
                'role': 'staff',
                'peetha': self.peetha.id
            }
        )
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_staff)
        self.assertTrue(PeethaHandler.objects.filter(user=test_user, peetha=self.peetha).exists())
        
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
        self.assertFalse(PeethaHandler.objects.filter(user=test_user).exists())

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

    def test_staff_peetha_lock_and_readonly(self):
        # Create another Peetha
        other_peetha = Peetha.objects.create(
            name='Balehonnur Peetha',
            slug='balehonnur',
            acharya='Soma Acharya',
            simhasana='Vajra Simhasana',
            location='Balehonnur',
            color='#FF0000'
        )
        
        # Create a Staff user assigned to self.peetha
        staff_user = User.objects.create_user(username='peethastaff', password='password123', is_staff=True)
        PeethaHandler.objects.create(user=staff_user, peetha=self.peetha)
        
        staff_client = Client()
        staff_client.login(username='peethastaff', password='password123')
        
        # 1. Staff accessing their own Peetha dashboard -> should succeed (200)
        response = staff_client.get(reverse('peethas:dashboard_peetha', kwargs={'slug': self.peetha.slug}))
        self.assertEqual(response.status_code, 200)
        
        # 2. Staff accessing other Peetha dashboard -> should return 403 Forbidden
        response = staff_client.get(reverse('peethas:dashboard_peetha', kwargs={'slug': other_peetha.slug}))
        self.assertEqual(response.status_code, 403)
        
        # 3. Staff trying to do write operation (e.g., updating live stream URL) on their own Peetha -> should return 403 Forbidden
        response = staff_client.post(
            reverse('peethas:update_peetha_live', kwargs={'slug': self.peetha.slug}),
            {'live_youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
        )
        self.assertEqual(response.status_code, 403)
        
    def test_bookings_blocked_for_staff_handlers_superadmins(self):
        # Find next Monday to make sure booking weekday validation passes
        today = datetime.date.today()
        days_ahead = (0 - today.weekday()) % 7
        next_monday = today + datetime.timedelta(days=days_ahead)
        next_monday_str = next_monday.strftime('%Y-%m-%d')
        
        # 1. Staff user booking attempt -> should return 403
        staff_user = User.objects.create_user(username='staff_booker', password='password123', is_staff=True)
        PeethaHandler.objects.create(user=staff_user, peetha=self.peetha)
        staff_client = Client()
        staff_client.login(username='staff_booker', password='password123')
        
        response = staff_client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Staff Booker',
                'devotee_phone': '1234567890',
                'date_of_pooja': next_monday_str
            }
        )
        self.assertEqual(response.status_code, 403)
        
        # 2. Handler user booking attempt -> should return 403
        handler_user = User.objects.create_user(username='handler_booker', password='password123')
        PeethaHandler.objects.create(user=handler_user, peetha=self.peetha)
        handler_client = Client()
        handler_client.login(username='handler_booker', password='password123')
        
        response = handler_client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Handler Booker',
                'devotee_phone': '1234567890',
                'date_of_pooja': next_monday_str
            }
        )
        self.assertEqual(response.status_code, 403)
        
        # 3. Superuser/Super Admin booking attempt -> should return 403
        super_user = User.objects.create_superuser(username='super_booker', password='password123', email='super_booker@example.com')
        super_client = Client()
        super_client.login(username='super_booker', password='password123')
        
        response = super_client.post(
            reverse('peethas:initiate_pooja_booking', kwargs={'peetha_slug': self.peetha.slug}),
            {
                'pooja_id': self.pooja.id,
                'devotee_name': 'Super Booker',
                'devotee_phone': '1234567890',
                'date_of_pooja': next_monday_str
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_dashboard_bookings_list_api(self):
        # Create a second Peetha and Pooja
        other_peetha = Peetha.objects.create(
            name='Balehonnur Peetha',
            slug='balehonnur',
            acharya='Soma Acharya',
            simhasana='Vajra Simhasana',
            location='Balehonnur',
            color='#FF0000'
        )
        other_pooja = Pooja.objects.create(
            peetha=other_peetha,
            name='Balehonnur Pooja',
            price=200.00,
            is_active=True
        )

        # Create a Handler assigned to self.peetha
        handler_user = User.objects.create_user(username='report_handler', password='password123')
        PeethaHandler.objects.create(user=handler_user, peetha=self.peetha)
        handler_client = Client()
        handler_client.login(username='report_handler', password='password123')

        # Create a Superuser
        admin_user = User.objects.create_superuser(username='report_admin', password='password123', email='report_admin@example.com')
        admin_client = Client()
        admin_client.login(username='report_admin', password='password123')

        # Create a devotee
        devotee_user = User.objects.create_user(username='report_devotee', password='password123')
        devotee_client = Client()
        devotee_client.login(username='report_devotee', password='password123')

        # 1. Devotee querying the API -> should return 403
        response = devotee_client.get(reverse('peethas:dashboard_bookings_list'))
        self.assertEqual(response.status_code, 403)

        # 2. Handler querying bookings without specific filters -> should return 200 (for their peetha only)
        response = handler_client.get(reverse('peethas:dashboard_bookings_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['peethas']), 1)
        self.assertEqual(data['peethas'][0]['slug'], self.peetha.slug)

        # 3. Handler querying booking list with pooja_id of their own Pooja -> should return 200
        response = handler_client.get(reverse('peethas:dashboard_bookings_list'), {'pooja_id': self.pooja.id})
        self.assertEqual(response.status_code, 200)

        # 4. Handler querying bookings for another Peetha's Pooja -> should return 403
        response = handler_client.get(reverse('peethas:dashboard_bookings_list'), {'pooja_id': other_pooja.id})
        self.assertEqual(response.status_code, 403)

        # 5. Super Admin querying any Pooja bookings -> should return 200
        response = admin_client.get(reverse('peethas:dashboard_bookings_list'), {'pooja_id': other_pooja.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['date_display'], 'All Dates')

        # 6. Super Admin querying with a specific date
        response = admin_client.get(reverse('peethas:dashboard_bookings_list'), {'date': '2026-06-25'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['date'], '2026-06-25')

        # 7. Super Admin querying with date ranges (3m, 6m, 12m)
        for r in ['3m', '6m', '9m', '12m', 'today', 'all']:
            response = admin_client.get(reverse('peethas:dashboard_bookings_list'), {'date_range': r})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('date_display', data)

    def test_staff_date_and_revenue_restrictions(self):
        # Create a booking for today
        today = datetime.date.today()
        booking_today = PoojaBooking.objects.create(
            user=self.user,
            pooja=self.pooja,
            devotee_name="Today Devotee",
            devotee_phone="9999999999",
            date_of_pooja=today,
            amount=500.00,
            payment_status="success"
        )
        # Create a booking for 5 days ago
        five_days_ago = today - datetime.timedelta(days=5)
        booking_past = PoojaBooking.objects.create(
            user=self.user,
            pooja=self.pooja,
            devotee_name="Past Devotee",
            devotee_phone="8888888888",
            date_of_pooja=five_days_ago,
            amount=300.00,
            payment_status="success"
        )

        # Create a Staff user assigned to self.peetha
        staff_user = User.objects.create_user(username='today_staff', password='password123', is_staff=True)
        PeethaHandler.objects.create(user=staff_user, peetha=self.peetha)
        staff_client = Client()
        staff_client.login(username='today_staff', password='password123')

        # 1. Staff queries bookings list API requesting date_range '3m'
        response = staff_client.get(reverse('peethas:dashboard_bookings_list'), {'date_range': '3m'})
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Date range must be overridden to 'today'
        self.assertEqual(data['date_range'], 'today')
        self.assertEqual(data['date_display'], today.strftime('%A, %d %B %Y'))

        # Revenue metrics must be strictly 0.0
        self.assertEqual(data['total_revenue'], 0.0)
        self.assertEqual(data['peethas'][0]['revenue'], 0.0)

        # Individual booking amounts must be 0.0 for staff
        bookings_returned = data['peethas'][0]['bookings']
        # Since staff is restricted to today, only today's booking should be returned
        self.assertEqual(len(bookings_returned), 1)
        self.assertEqual(bookings_returned[0]['devotee_name'], "Today Devotee")
        self.assertEqual(bookings_returned[0]['amount'], 0.0)

        # 2. Peetha Handler queries bookings list API requesting date_range '3m'
        handler_user = User.objects.create_user(username='date_handler', password='password123')
        PeethaHandler.objects.create(user=handler_user, peetha=self.peetha)
        handler_client = Client()
        handler_client.login(username='date_handler', password='password123')

        response = handler_client.get(reverse('peethas:dashboard_bookings_list'), {'date_range': '3m'})
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Date range and revenue must NOT be overridden or zeroed out
        self.assertEqual(data['date_range'], '3m')
        self.assertEqual(data['total_revenue'], 800.0)
        self.assertEqual(data['peethas'][0]['revenue'], 800.0)

        bookings_returned = data['peethas'][0]['bookings']
        self.assertEqual(len(bookings_returned), 2)
        # Amounts must be correct actual amounts for handler
        for b in bookings_returned:
            if b['devotee_name'] == "Today Devotee":
                self.assertEqual(b['amount'], 500.0)
            elif b['devotee_name'] == "Past Devotee":
                self.assertEqual(b['amount'], 300.0)


class DevoteeRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Ensure DEVOTEE_REGISTRATION flag object is created (defaulting to is_enabled=True)
        self.flag, _ = FeatureFlag.objects.get_or_create(
            name='DEVOTEE_REGISTRATION',
            defaults={'is_enabled': True, 'description': 'Allow devotee registration'}
        )

    def test_registration_enabled_by_default(self):
        # When devotee registration is enabled, visiting register page should return 200
        response = self.client.get(reverse('peethas:register'))
        self.assertEqual(response.status_code, 200)

        # A post request should successfully register a new user
        response = self.client.post(
            reverse('peethas:register'),
            {
                'username': 'newdevotee',
                'first_name': 'New Devotee',
                'email': 'newdevotee@example.com',
                'password': 'password123'
            }
        )
        self.assertEqual(response.status_code, 302) # redirects to home
        self.assertTrue(User.objects.filter(username='newdevotee').exists())

    def test_registration_disabled(self):
        # Disable devotee registration flag
        self.flag.is_enabled = False
        self.flag.save()

        # Visiting register page should redirect to login
        response = self.client.get(reverse('peethas:register'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        # Attempting to post to register should also redirect and not create a user
        response = self.client.post(
            reverse('peethas:register'),
            {
                'username': 'blockeddevotee',
                'first_name': 'Blocked Devotee',
                'email': 'blocked@example.com',
                'password': 'password123'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='blockeddevotee').exists())


class UserBirthdayWishTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='birthdayuser', password='password123')
        self.client = Client()
        self.client.login(username='birthdayuser', password='password123')
        # Ensure profile exists
        self.profile = self.user.profile

    def test_no_birthday_wish_when_dob_not_set(self):
        self.profile.date_of_birth = None
        self.profile.save()

        response = self.client.get(reverse('peethas:home'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_birthday'])
        self.assertNotContains(response, 'id="birthdayModal"')

    def test_no_birthday_wish_on_different_day(self):
        today = datetime.date.today()
        # Set birthday to yesterday
        different_day = today - datetime.timedelta(days=1)
        self.profile.date_of_birth = different_day
        self.profile.save()

        response = self.client.get(reverse('peethas:home'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_birthday'])
        self.assertNotContains(response, 'id="birthdayModal"')

    def test_birthday_wish_on_birthday(self):
        today = datetime.date.today()
        # Set birthday to today (year 1995)
        birthday_today = datetime.date(1995, today.month, today.day)
        self.profile.date_of_birth = birthday_today
        self.profile.save()

        response = self.client.get(reverse('peethas:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_birthday'])
        self.assertContains(response, 'id="birthdayModal"')


from peethas.models import Building, Room, AccommodationBooking

class AccommodationBookingTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='devotee1', password='password123')
        # Create Peetha
        self.peetha = Peetha.objects.create(
            name='Kedar Peetha',
            slug='kedar',
            acharya='Jagadguru Kedar',
            simhasana='Himavat Simhasana',
            location='Kedarnath',
            color='#008080'
        )
        # Create a Building
        # Ground floor = floor 0. We'll have 2 floors, 3 rooms per floor, 1 AC floor (Ground floor will be AC)
        self.building = Building.objects.create(
            peetha=self.peetha,
            name='Yatri Niwas Kedar',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1,
            ac_room_price=1200.00,
            ordinary_room_price=600.00
        )
        
    def test_room_autogenerated_successfully(self):
        # Building should have generated 6 rooms (floor 0: G1, G2, G3; floor 1: 101, 102, 103)
        self.assertEqual(Room.objects.filter(building=self.building).count(), 6)
        
        # Floor 0 rooms should be AC
        ac_rooms = Room.objects.filter(building=self.building, room_type='AC')
        self.assertEqual(ac_rooms.count(), 3)
        self.assertTrue(all(r.room_number in ['G1', 'G2', 'G3'] for r in ac_rooms))
        self.assertEqual(ac_rooms.first().price_per_night, 1200.00)
        
        # Floor 1 rooms should be Ordinary
        ord_rooms = Room.objects.filter(building=self.building, room_type='Ordinary')
        self.assertEqual(ord_rooms.count(), 3)
        self.assertTrue(all(r.room_number in ['101', '102', '103'] for r in ord_rooms))
        self.assertEqual(ord_rooms.first().price_per_night, 600.00)

    def test_stay_availability_endpoint(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        # Query availability before any bookings
        url = reverse('peethas:accommodation_availability', kwargs={'peetha_slug': self.peetha.slug})
        response = self.client.get(f"{url}?check_in={today}&check_out={tomorrow}")
        self.assertEqual(response.status_code, 200)
        data = response.json()['availability']
        
        # Both types should have 3 rooms pending
        self.assertEqual(data['AC']['available_count'], 3)
        self.assertEqual(data['Ordinary']['available_count'], 3)
        self.assertEqual(data['AC']['price_per_night'], 1200.00)
        self.assertEqual(data['Ordinary']['price_per_night'], 600.00)

    def test_overlapping_stay_booking_reduces_availability(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        day_after = today + datetime.timedelta(days=2)
        
        # Create an active booking for an AC room today to tomorrow
        room = Room.objects.filter(building=self.building, room_type='AC').first()
        AccommodationBooking.objects.create(
            user=self.user,
            peetha=self.peetha,
            room=room,
            room_type='AC',
            devotee_name='Devotee A',
            devotee_phone='9876543210',
            check_in_date=today,
            check_out_date=tomorrow,
            amount=1200.00,
            payment_status='success'
        )
        
        # Query availability for today -> tomorrow
        url = reverse('peethas:accommodation_availability', kwargs={'peetha_slug': self.peetha.slug})
        response = self.client.get(f"{url}?check_in={today}&check_out={tomorrow}")
        data = response.json()['availability']
        
        # AC available count should drop to 2, Ordinary still 3
        self.assertEqual(data['AC']['available_count'], 2)
        self.assertEqual(data['Ordinary']['available_count'], 3)
        
        # Query availability for tomorrow -> day_after
        response_next_day = self.client.get(f"{url}?check_in={tomorrow}&check_out={day_after}")
        data_next_day = response_next_day.json()['availability']
        
        # No overlap, so both should have 3
        self.assertEqual(data_next_day['AC']['available_count'], 3)
        self.assertEqual(data_next_day['Ordinary']['available_count'], 3)

    def test_stay_booking_via_post_works_and_allocates_room(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        self.client.login(username='devotee1', password='password123')
        
        # Post booking request
        url = reverse('peethas:initiate_accommodation_booking', kwargs={'peetha_slug': self.peetha.slug})
        post_data = {
            'devotee_name': 'Test Devotee Stay',
            'devotee_phone': '9999988888',
            'devotee_email': 'test@devotee.com',
            'room_type': 'Ordinary',
            'check_in_date': today.strftime('%Y-%m-%d'),
            'check_out_date': tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(url, post_data)
        
        # Should redirect to receipt success page
        self.assertEqual(response.status_code, 302)
        booking = AccommodationBooking.objects.get(devotee_name='Test Devotee Stay')
        
        # Check that room was allocated in the background and is Ordinary
        self.assertIsNotNone(booking.room)
        self.assertEqual(booking.room.room_type, 'Ordinary')
        self.assertTrue(booking.room.room_number in ['101', '102', '103'])
        self.assertEqual(booking.amount, 600.00)
        self.assertEqual(booking.payment_status, 'success')

    def test_custom_ac_room_numbers_generation(self):
        # Create a building with explicit ac_room_numbers override
        b_custom = Building.objects.create(
            peetha=self.peetha,
            name='Custom AC Building',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1, # normally Floor 0 is AC (G1, G2, G3)
            ac_room_numbers='G1, 102', # custom list overrides floor count
            ac_room_price=1500.00,
            ordinary_room_price=700.00
        )
        
        # Total rooms should still be 6
        self.assertEqual(Room.objects.filter(building=b_custom).count(), 6)
        
        # Only G1 and 102 should be AC
        ac_rooms = Room.objects.filter(building=b_custom, room_type='AC')
        self.assertEqual(ac_rooms.count(), 2)
        self.assertTrue(all(r.room_number in ['G1', '102'] for r in ac_rooms))
        
        # The other 4 rooms should be Ordinary
        ord_rooms = Room.objects.filter(building=b_custom, room_type='Ordinary')
        self.assertEqual(ord_rooms.count(), 4)
        self.assertTrue(all(r.room_number in ['G2', 'G3', '101', '103'] for r in ord_rooms))

    def test_hot_water_configs_returned_correctly(self):
        # Update building with hot water settings
        self.building.has_hot_water = True
        self.building.hot_water_timings = '6:00 AM - 9:00 AM'
        self.building.save()
        
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        url = reverse('peethas:accommodation_availability', kwargs={'peetha_slug': self.peetha.slug})
        response = self.client.get(f"{url}?check_in={today}&check_out={tomorrow}")
        self.assertEqual(response.status_code, 200)
        data = response.json()['availability']
        
        # Both AC and Ordinary have rooms in self.building, so both should have hot water info
        self.assertTrue(data['AC']['hot_water_available'])
        self.assertEqual(data['AC']['hot_water_timings'], '6:00 AM - 9:00 AM')
        self.assertTrue(data['Ordinary']['hot_water_available'])
        self.assertEqual(data['Ordinary']['hot_water_timings'], '6:00 AM - 9:00 AM')


class BuildingCrudTestCase(TestCase):
    def setUp(self):
        # Create Peetha
        self.peetha = Peetha.objects.create(
            name='Kedar Peetha',
            slug='kedar',
            acharya='Jagadguru Kedar',
            simhasana='Himavat Simhasana',
            location='Kedarnath',
            color='#008080'
        )
        # Create Superuser (Admin)
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')
        # Create Handler user
        self.handler_user = User.objects.create_user(username='handler', password='password123')
        PeethaHandler.objects.create(user=self.handler_user, peetha=self.peetha)
        # Create Staff user (is_staff=True, linked to Peetha, should be able to edit building info)
        self.staff_user = User.objects.create_user(username='staff_handler', password='password123', is_staff=True)
        PeethaHandler.objects.create(user=self.staff_user, peetha=self.peetha)
        # Create Devotee user (not authorized to manage buildings)
        self.devotee = User.objects.create_user(username='devotee', password='password123')
        
        self.client = Client()

    def test_building_add_unauthorized(self):
        # Devotee tries to add building -> should fail with 403
        self.client.login(username='devotee', password='password123')
        url = reverse('peethas:building_add', kwargs={'slug': self.peetha.slug})
        response = self.client.post(url, {
            'name': 'Unauthorized Building',
            'total_floors': 2,
            'rooms_per_floor': 3,
            'ac_floors_count': 1,
            'ac_room_price': 1000,
            'ordinary_room_price': 500,
            'is_active': True
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Building.objects.count(), 0)

    def test_building_add_authorized(self):
        self.client.login(username='handler', password='password123')
        url = reverse('peethas:building_add', kwargs={'slug': self.peetha.slug})
        response = self.client.post(url, {
            'name': 'Handler Building',
            'total_floors': 3,
            'rooms_per_floor': 2,
            'ac_floors_count': 1,
            'ac_room_price': 1200.00,
            'ordinary_room_price': 600.00,
            'is_active': True
        })
        self.assertEqual(response.status_code, 302) # redirects to dashboard
        
        # Verify building created
        building = Building.objects.get(name='Handler Building')
        self.assertEqual(building.peetha, self.peetha)
        
        # Verify rooms generated (3 floors * 2 rooms = 6 rooms)
        self.assertEqual(Room.objects.filter(building=building).count(), 6)
        # Floor 0: G1, G2 (AC)
        # Floor 1: 101, 102 (Ordinary)
        # Floor 2: 201, 202 (Ordinary)
        ac_rooms = Room.objects.filter(building=building, room_type='AC')
        self.assertEqual(ac_rooms.count(), 2)
        self.assertTrue(all(r.room_number in ['G1', 'G2'] for r in ac_rooms))
        self.assertEqual(ac_rooms.first().price_per_night, 1200.00)

    def test_building_edit_updates_rooms(self):
        # Create a building first
        building = Building.objects.create(
            peetha=self.peetha,
            name='Test Building',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1,
            ac_room_price=1000.00,
            ordinary_room_price=500.00
        )
        self.assertEqual(Room.objects.filter(building=building).count(), 6)
        
        self.client.login(username='handler', password='password123')
        url = reverse('peethas:building_edit', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        
        # Edit: update prices, increase rooms_per_floor to 4, increase AC floors to 2
        response = self.client.post(url, {
            'name': 'Updated Test Building',
            'description': 'New desc',
            'total_floors': 2,
            'rooms_per_floor': 4,
            'ac_floors_count': 2,
            'ac_room_price': 1500.00,
            'ordinary_room_price': 800.00,
            'is_active': True
        })
        self.assertEqual(response.status_code, 302)
        
        building.refresh_from_db()
        self.assertEqual(building.name, 'Updated Test Building')
        self.assertEqual(building.rooms_per_floor, 4)
        
        # Verify rooms count (2 floors * 4 rooms = 8 rooms)
        self.assertEqual(Room.objects.filter(building=building).count(), 8)
        # All floors are AC now since ac_floors_count = 2 (floors 0 and 1)
        ac_rooms = Room.objects.filter(building=building, room_type='AC')
        self.assertEqual(ac_rooms.count(), 8)
        self.assertEqual(ac_rooms.first().price_per_night, 1500.00)

    def test_building_edit_layout_pruning_with_bookings(self):
        # Create building
        building = Building.objects.create(
            peetha=self.peetha,
            name='Pruning Building',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1,
            ac_room_price=1000.00,
            ordinary_room_price=500.00
        )
        
        # Create booking for Room 101 (floor 1, ordinary)
        room_101 = Room.objects.get(building=building, room_number='101')
        AccommodationBooking.objects.create(
            user=self.devotee,
            peetha=self.peetha,
            room=room_101,
            room_type='Ordinary',
            devotee_name='Devotee B',
            devotee_phone='1234567890',
            check_in_date=datetime.date.today(),
            check_out_date=datetime.date.today() + datetime.timedelta(days=1),
            amount=500.00,
            payment_status='success'
        )
        
        self.client.login(username='handler', password='password123')
        url = reverse('peethas:building_edit', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        
        # Try to decrease total_floors to 1. This would prune floor 1, including Room 101.
        # It should fail because Room 101 has a booking and room delete is PROTECTed.
        response = self.client.post(url, {
            'name': 'Pruning Building',
            'total_floors': 1,
            'rooms_per_floor': 3,
            'ac_floors_count': 1,
            'ac_room_price': 1000.00,
            'ordinary_room_price': 500.00,
            'is_active': True
        })
        # It should re-render the edit form with an error (200) rather than redirecting (302)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cannot update building layout")
        
        # Verify building total floors remains 2
        building.refresh_from_db()
        self.assertEqual(building.total_floors, 2)

    def test_building_delete(self):
        building = Building.objects.create(
            peetha=self.peetha,
            name='Delete Building',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1,
            ac_room_price=1000.00,
            ordinary_room_price=500.00
        )
        self.assertEqual(Room.objects.filter(building=building).count(), 6)
        
        self.client.login(username='handler', password='password123')
        url = reverse('peethas:building_delete', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Building.objects.filter(pk=building.pk).count(), 0)
        self.assertEqual(Room.objects.filter(building=building).count(), 0)

    def test_building_delete_protected_with_booking(self):
        building = Building.objects.create(
            peetha=self.peetha,
            name='Delete Protected Building',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1,
            ac_room_price=1000.00,
            ordinary_room_price=500.00
        )
        
        # Create booking for Room G1 (floor 0, AC)
        room_g1 = Room.objects.get(building=building, room_number='G1')
        AccommodationBooking.objects.create(
            user=self.devotee,
            peetha=self.peetha,
            room=room_g1,
            room_type='AC',
            devotee_name='Devotee C',
            devotee_phone='1234567890',
            check_in_date=datetime.date.today(),
            check_out_date=datetime.date.today() + datetime.timedelta(days=1),
            amount=1000.00,
            payment_status='success'
        )
        
        self.client.login(username='handler', password='password123')
        url = reverse('peethas:building_delete', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        # Verify building and rooms NOT deleted
        self.assertEqual(Building.objects.filter(pk=building.pk).count(), 1)
        self.assertEqual(Room.objects.filter(building=building).count(), 6)

    def test_building_add_staff_authorized(self):
        # Staff user should be authorized to add building
        self.client.login(username='staff_handler', password='password123')
        url = reverse('peethas:building_add', kwargs={'slug': self.peetha.slug})
        response = self.client.post(url, {
            'name': 'Staff Building',
            'total_floors': 2,
            'rooms_per_floor': 3,
            'ac_floors_count': 1,
            'ac_room_price': 1100.00,
            'ordinary_room_price': 550.00,
            'is_active': True
        })
        self.assertEqual(response.status_code, 302) # redirects to dashboard
        building = Building.objects.get(name='Staff Building')
        self.assertEqual(building.peetha, self.peetha)
        self.assertEqual(Room.objects.filter(building=building).count(), 6)

    def test_building_edit_staff_authorized(self):
        building = Building.objects.create(
            peetha=self.peetha,
            name='Test Building to Edit',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1,
            ac_room_price=1000.00,
            ordinary_room_price=500.00
        )
        self.client.login(username='staff_handler', password='password123')
        url = reverse('peethas:building_edit', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        response = self.client.post(url, {
            'name': 'Edited By Staff',
            'description': 'Staff edited desc',
            'total_floors': 2,
            'rooms_per_floor': 3,
            'ac_floors_count': 1,
            'ac_room_price': 1100.00,
            'ordinary_room_price': 550.00,
            'is_active': True
        })
        self.assertEqual(response.status_code, 302)
        building.refresh_from_db()
        self.assertEqual(building.name, 'Edited By Staff')

    def test_building_delete_staff_authorized(self):
        building = Building.objects.create(
            peetha=self.peetha,
            name='Test Building to Delete',
            total_floors=2,
            rooms_per_floor=3,
            ac_floors_count=1,
            ac_room_price=1000.00,
            ordinary_room_price=500.00
        )
        self.client.login(username='staff_handler', password='password123')
        url = reverse('peethas:building_delete', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Building.objects.filter(pk=building.pk).count(), 0)

    def test_building_actions_admin_superuser_authorized(self):
        # Admin (superuser) should be authorized for add
        self.client.login(username='admin', password='password123')
        url_add = reverse('peethas:building_add', kwargs={'slug': self.peetha.slug})
        response_add = self.client.post(url_add, {
            'name': 'Admin Building',
            'total_floors': 2,
            'rooms_per_floor': 3,
            'ac_floors_count': 1,
            'ac_room_price': 1000.00,
            'ordinary_room_price': 500.00,
            'is_active': True
        })
        self.assertEqual(response_add.status_code, 302)
        building = Building.objects.get(name='Admin Building')
        
        # Admin (superuser) should be authorized for edit
        url_edit = reverse('peethas:building_edit', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        response_edit = self.client.post(url_edit, {
            'name': 'Admin Building Edited',
            'description': 'Edited desc',
            'total_floors': 2,
            'rooms_per_floor': 3,
            'ac_floors_count': 1,
            'ac_room_price': 1000.00,
            'ordinary_room_price': 500.00,
            'is_active': True
        })
        self.assertEqual(response_edit.status_code, 302)
        building.refresh_from_db()
        self.assertEqual(building.name, 'Admin Building Edited')

        # Admin (superuser) should be authorized for delete
        url_delete = reverse('peethas:building_delete', kwargs={'slug': self.peetha.slug, 'pk': building.pk})
        response_delete = self.client.post(url_delete)
        self.assertEqual(response_delete.status_code, 302)
        self.assertEqual(Building.objects.filter(pk=building.pk).count(), 0)


from io import BytesIO

class DynamicContentTestCase(TestCase):
    def setUp(self):
        # Create Superuser (Admin)
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')
        # Create Devotee user
        self.devotee = User.objects.create_user(username='devotee', password='password123')
        
        self.client = Client()

    def test_dynamic_content_fallback(self):
        # By default, helpers should return static dictionary contents
        from .views import get_dynamic_heritage_content, get_dynamic_veerashaiva_content
        from .heritage_content import HERITAGE_CONTENT
        from .veerashaiva_content import VEERASHAIVA_CONTENT
        
        heritage = get_dynamic_heritage_content('en')
        self.assertEqual(heritage['title'], HERITAGE_CONTENT['en']['title'])
        self.assertEqual(heritage['conclusion'], HERITAGE_CONTENT['en']['conclusion'])
        
        veerashaiva = get_dynamic_veerashaiva_content('kn')
        self.assertEqual(veerashaiva['title'], VEERASHAIVA_CONTENT['kn']['title'])

    def test_update_dynamic_content_unauthorized(self):
        # Devotee tries to update content -> should fail with 403
        self.client.login(username='devotee', password='password123')
        url = reverse('peethas:update_dynamic_content')
        response = self.client.post(url, {
            'section': 'heritage',
            'lang': 'en',
            'title': 'Test Title'
        })
        self.assertEqual(response.status_code, 403)

    def test_update_dynamic_content_success_manual(self):
        self.client.login(username='admin', password='password123')
        url = reverse('peethas:update_dynamic_content')
        
        # Post new heritage configuration
        response = self.client.post(url, {
            'section': 'heritage',
            'lang': 'en',
            'title': 'Custom Heritage Title',
            'conclusion': 'Custom Heritage Conclusion',
            'shloka_verse': 'Verse text here',
            'shloka_reference': 'Reference source here',
            'intro_paragraphs_text': "Para one.\n\nPara two."
        })
        
        # Should redirect back to dashboard
        self.assertEqual(response.status_code, 302)
        
        # Verify database objects created
        from .models import DynamicContentMeta, DynamicParagraph
        meta = DynamicContentMeta.objects.get(section='heritage', language='en')
        self.assertEqual(meta.title, 'Custom Heritage Title')
        self.assertEqual(meta.conclusion, 'Custom Heritage Conclusion')
        
        paras = DynamicParagraph.objects.filter(section='heritage_intro', language='en')
        self.assertEqual(paras.count(), 2)
        self.assertEqual(paras[0].text, 'Para one.')
        self.assertEqual(paras[1].text, 'Para two.')

    def test_update_dynamic_content_file_upload(self):
        self.client.login(username='admin', password='password123')
        url = reverse('peethas:update_dynamic_content')
        
        # Create a mock text file
        file_data = b"This is uploaded paragraph one.\n\nThis is uploaded paragraph two."
        mock_file = BytesIO(file_data)
        mock_file.name = "paragraphs.txt"
        
        response = self.client.post(url, {
            'section': 'heritage',
            'lang': 'en',
            'title': 'Custom Heritage Title File',
            'intro_paragraphs_file': mock_file
        })
        
        self.assertEqual(response.status_code, 302)
        
        from .models import DynamicParagraph
        paras = DynamicParagraph.objects.filter(section='heritage_intro', language='en')
        self.assertEqual(paras.count(), 2)
        self.assertEqual(paras[0].text, 'This is uploaded paragraph one.')
        self.assertEqual(paras[1].text, 'This is uploaded paragraph two.')
        
    def test_get_dynamic_content_api(self):
        # Populate database record
        from .models import DynamicContentMeta, DynamicParagraph
        DynamicContentMeta.objects.create(
            section='heritage',
            language='en',
            title='API Title Test',
            conclusion='API Conclusion Test',
            shloka_verse='API Verse Test',
            shloka_reference='API Reference Test'
        )
        DynamicParagraph.objects.create(
            section='heritage_intro',
            language='en',
            order=0,
            text='API Para Test'
        )
        
        self.client.login(username='admin', password='password123')
        url = reverse('peethas:get_dynamic_content_api')
        response = self.client.get(url, {'section': 'heritage', 'lang': 'en'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], 'API Title Test')
        self.assertEqual(data['conclusion'], 'API Conclusion Test')
        self.assertEqual(data['shloka_verse'], 'API Verse Test')
        self.assertEqual(data['intro_paragraphs'], 'API Para Test')


class YouTubeURLTestCase(TestCase):
    def test_live_youtube_id_extraction(self):
        peetha = Peetha(
            name='Test Peetha',
            slug='test-peetha',
            live_youtube_url='https://youtube.com/live/ZI1v_UvYj34?feature=share'
        )
        self.assertEqual(peetha.get_live_youtube_id(), 'ZI1v_UvYj34')

    def test_other_youtube_formats_extraction(self):
        peetha = Peetha(name='Test', slug='test')
        
        # Test standard watch
        peetha.live_youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        self.assertEqual(peetha.get_live_youtube_id(), 'dQw4w9WgXcQ')
        
        # Test short URL
        peetha.live_youtube_url = 'https://youtu.be/dQw4w9WgXcQ'
        self.assertEqual(peetha.get_live_youtube_id(), 'dQw4w9WgXcQ')
        
        # Test embed URL
        peetha.live_youtube_url = 'https://www.youtube.com/embed/dQw4w9WgXcQ'
        self.assertEqual(peetha.get_live_youtube_id(), 'dQw4w9WgXcQ')
        
        # Test shorts URL
        peetha.live_youtube_url = 'https://youtube.com/shorts/dQw4w9WgXcQ'
        self.assertEqual(peetha.get_live_youtube_id(), 'dQw4w9WgXcQ')









