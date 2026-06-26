# Global Feature Flags for Pancha Peethas Application

class DynamicFeatureFlag:
    def __init__(self, name, default=True):
        self.name = name
        self.default = default

    def __bool__(self):
        try:
            from .models import FeatureFlag
            flag = FeatureFlag.objects.get(name=self.name)
            return flag.is_enabled
        except Exception:
            return self.default

    def __str__(self):
        return str(bool(self))


# Toggle between Rectangular and Circular portraits on the Home Page
USE_RECTANGULAR_PORTRAITS = DynamicFeatureFlag('USE_RECTANGULAR_PORTRAITS', True)

# Global Devotee Registration Flag
DEVOTEE_REGISTRATION = DynamicFeatureFlag('DEVOTEE_REGISTRATION', True)

