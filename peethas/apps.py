from django.apps import AppConfig


class PeethasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'peethas'

    def ready(self):
        import firebase_admin
        from firebase_admin import credentials
        from django.conf import settings
        import os

        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            # Get path to the service account JSON file
            cred_path = os.path.join(settings.BASE_DIR, 'pancha-peethas-firebase-adminsdk-fbsvc-eb635ddb1f.json')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                print("WARNING: Firebase Admin SDK credentials not found at:", cred_path)
