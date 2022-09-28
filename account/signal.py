from .customsignal import blacklist_update, User_Consent
from django.dispatch import receiver
from .models import *
from shops.models import *


@receiver(blacklist_update, sender=CustomUser)
def blacklist_log(sender, **kwargs):
    if not sender.activate:
        BlackListHistory.objects.create(
            blacklist=sender,
            content="관리자에 의해 블랙리스트에 등록되었습니다.",
            date=True,
        )
    else:
        BlackListHistory.objects.create(
            blacklist=sender,
            content="관리자에 의해 블랙리스트에 해제되었습니다.",
            date=True,
        )

@receiver(User_Consent, sender=CustomUser)
def user_consent(sender, **kwargs):
    print("")
blacklist_update.connect(blacklist_log)
