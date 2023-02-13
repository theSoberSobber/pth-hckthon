from django.conf import settings
import os, random
from .models import UserAuthPassPoint
from django.contrib.auth.models import User

def getMediaImageList(user=None):
    if user:
        user_obj = User.objects.get(username=user)
        auth_passpoint_obj = UserAuthPassPoint.objects.get(user=user_obj)
        auth_image_list = auth_passpoint_obj.auth_images.split(",")
    random_image_url = []
    for file in os.listdir(settings.MEDIA_ROOT):
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            img_url = "/media/"+file
            if user:
                if img_url not in auth_image_list:
                    random_image_url.append(img_url)
            else:
                random_image_url.append(img_url)

    if user:
        random.shuffle(random_image_url)
        imgset1 = random_image_url[:8]
        imgset1.append(auth_image_list[0])

        random.shuffle(random_image_url)
        imgset2 = random_image_url[:8]
        imgset2.append(auth_image_list[1])

        random.shuffle(random_image_url)
        imgset3 = random_image_url[:8]
        imgset3.append(auth_image_list[2])
    else:
        random.shuffle(random_image_url)
        imgset1 = random_image_url[:9]
        random.shuffle(random_image_url)
        imgset2 = random_image_url[:9]
        random.shuffle(random_image_url)
        imgset3 = random_image_url[:9]

    random.shuffle(imgset1)
    random.shuffle(imgset2)
    random.shuffle(imgset3)

    return imgset1, imgset2, imgset3