"""Historical V11 mocked replay preserves its original qualified DATA identity."""
from tests import test_photo_nape_metadata_boundary_history as historical


class LatestMetadataBoundaryHistoryTests(historical.NapeMetadataBoundaryHistoryTests):
    version = 11
