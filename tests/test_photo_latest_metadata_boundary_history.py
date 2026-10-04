"""Latest qualified DATA advances current dispatch; V10 keeps its old outcome."""
from tests import test_photo_nape_metadata_boundary_history as historical


class LatestMetadataBoundaryHistoryTests(historical.NapeMetadataBoundaryHistoryTests):
    version = 11
