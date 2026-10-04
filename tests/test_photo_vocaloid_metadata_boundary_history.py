"""The merged current boundary keeps every semantic field of V11 intact."""
from tests import test_photo_nape_metadata_boundary_history as historical


class VocaloidMetadataBoundaryHistoryTests(historical.NapeMetadataBoundaryHistoryTests):
    version = 12
