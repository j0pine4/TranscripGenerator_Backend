from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle, AnonRateThrottle, BaseThrottle
from UserAuth.models import SUBSCRIPTION_TIERS_ENUM, SUBSCRIPTION_TIERS

class Transcript_Throttle(UserRateThrottle):
    def allow_request(self, request, view):

        user = request.user

        if user.is_authenticated:
            if user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.FREE.value:
                self.rate = '15/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.PREMIUM.value:
                self.rate = '30/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ENHANCED.value:
                self.rate = '50/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ULTIMATE.value:
                self.rate = '100/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ADMIN.value:
                self.rate = '100/minute'
        else:
            self.rate = '10/day'

            
        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)
    
class Generator_Throttle(UserRateThrottle):
    def allow_request(self, request, view):

        user = request.user

        if user.is_authenticated:
            if user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.FREE.value:
                self.rate = '5/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.PREMIUM.value:
                self.rate = '15/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ENHANCED.value:
                self.rate = '25/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ULTIMATE.value:
                self.rate = '50/day'
            elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ADMIN.value:
                self.rate = '100/minute'
        else:
            self.rate = '5/day'

        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)
