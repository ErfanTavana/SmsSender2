import re

def normalize_phone_number(phone_number):
    """
    Normalize and validate Iranian phone numbers.
    Returns the phone number in standard format (e.g., 09xxxxxxxxx).
    """
    # حذف فاصله‌ها و خط تیره‌های اضافی
    phone_number = re.sub(r'\s+|-', '', phone_number)  # استفاده از regex برای حذف فاصله و خط تیره

    # الگوی regex برای بررسی فرمت شماره تلفن
    pattern = r'^(?:\+98|0098|98|0)?(9\d{9})$'

    # بررسی فرمت‌های معتبر
    if re.match(r'^(09\d{9})$', phone_number):
        return phone_number  # فرمت درست
    elif re.match(pattern, phone_number):
        # تبدیل به فرمت استاندارد (09xxxxxxxxx)
        if phone_number.startswith('+98'):
            return '0' + phone_number[3:]
        elif phone_number.startswith('0098'):
            return '0' + phone_number[4:]
        elif phone_number.startswith('98'):
            return '0' + phone_number[2:]
    else:
        raise ValueError("شماره تلفن معتبر نیست. شماره تلفن باید یک شماره معتبر ایرانی باشد.")
