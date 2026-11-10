from vendor.models import Vendor
from accounts.models import UserProfile


def get_vendor(request):
    """
    AnonymousUser, Customer এবং Vendor সবার জন্য সেফ হ্যান্ডলিং।
    কোনো এরর ছাড়াই টেমপ্লেটে vendor এবং user_profile অবজেক্ট পাঠায়।
    """
    # ১. ইউজার লগইন না থাকলে (AnonymousUser) সরাসরি None রিটার্ন করবে
    if not request.user.is_authenticated:
        return {
            'vendor': None,
            'user_profile': None,
        }

    # ২. ইউজার লগইন থাকলে তার ভেন্ডর ডাটা খোঁজা
    try:
        vendor = Vendor.objects.get(user=request.user)
    except (Vendor.DoesNotExist, AttributeError):
        vendor = None

    # ৩. ইউজারের প্রোফাইল ডাটা খোঁজা
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, AttributeError):
        user_profile = None

    return {
        'vendor': vendor,
        'user_profile': user_profile,
    }