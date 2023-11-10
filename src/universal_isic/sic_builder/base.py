class Base_Classification:
    def __init__(self, number_of_levels: int, *args, **kwargs):
        self.number_of_levels = number_of_levels

    def get_elements(*args, **kwargs):
        raise NotImplementedError("Implement it in the legacy class")
