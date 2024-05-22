class SerializerMixin:
    """
    Mixin pour récupérer la classe sérialiseur appropriée
    en fonction de l'action de la vue.
    """

    serializer_mapping = {
        "list": None,
        "retrieve": None,
        "create": None,
        "update": None,
        "partial_update": None,
    }

    def get_serializer_class(self):
        """
        Retourne la classe sérialiseur appropriée en fonction de l'action de la vue.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)
