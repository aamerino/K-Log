from KLog.views import FileUpload
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'fileupload', FileUpload)
urlpatterns = router.urls