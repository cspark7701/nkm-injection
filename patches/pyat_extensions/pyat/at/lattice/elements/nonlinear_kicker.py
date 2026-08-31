import numpy as np
from .element_object import Element

class NonlinearKicker(Element):
    """
    A custom nonlinear kicker element for AT, using pyNKMPass.
    
    Attributes:
        FamName (str): The family name of the element.
        Length (float): The length of the kicker magnet (m).
        FieldMap (numpy.ndarray): 3D field map loaded from Radia.
    """
    _BUILD_ATTRIBUTES = Element._BUILD_ATTRIBUTES + ["Length", "Energy", "Nslice", "Filename_in"]

    def __init__(self, family_name: str, Length: float, Energy: float, Nslice: int, **kwargs):
        """Initialize the nonlinear kicker element."""
        Filename_in = kwargs.pop("Filename_in", None)
        field_map = self.fieldmap_from_file(Filename_in) if Filename_in else None
        kwargs.setdefault("PassMethod", "pyNKMPass")
        
        super().__init__(family_name, Length=Length, Energy=Energy, Nslice=Nslice, **kwargs)
        
        # Store additional attributes
        self.Filename_in = Filename_in
        self.FieldMap = field_map
        self.Length = Length
        self.Energy = Energy
        self.Nslice = Nslice
    
    @staticmethod    
    def fieldmap_from_file(Filename_in):
        """Load nonlinear kicker field map from file."""
        if Filename_in is None:
            raise ValueError("Filename_in must be provided to load field map.")
        
        return np.load(Filename_in)  # Load the precomputed 3D field
