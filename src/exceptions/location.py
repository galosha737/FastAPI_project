class LocationNotFound(Exception):
    def __init__(self, location_id: int):
        self.location_id = location_id
        super().__init__(f'Location with id={location_id} not found')
