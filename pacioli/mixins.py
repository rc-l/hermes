class PagePinningMixin(object):
    """Mixin to set the the pinning page in the session"""

    def get(self, request, *args, **kwargs):
        """
        Override get to manipulate cookies
        """
        request.session["pinned_page"] = request.path
        return super().get(self, request, *args, **kwargs)
