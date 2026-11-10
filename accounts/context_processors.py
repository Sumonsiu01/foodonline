from vendor.models import Vendor

def get_vendor(request):
    
    if request.user.is_authenticated:
        try:
            vendor = Vendor.objects.get(user=request.user)
            return dict(vendor=vendor)
        except Vendor.DoesNotExist:
            return dict(vendor=None)
    

    return dict(vendor=None)