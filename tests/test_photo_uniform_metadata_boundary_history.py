"""The uniform successor preserves every semantic field of V12."""
from tests import test_photo_nape_metadata_boundary_history as historical


class UniformMetadataBoundaryHistoryTests(historical.NapeMetadataBoundaryHistoryTests):
    version = 13
