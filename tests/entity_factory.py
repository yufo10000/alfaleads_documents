class CopyDocumentsFactoryMixin:
    def copy_object(self, object):
        return object.copy()
