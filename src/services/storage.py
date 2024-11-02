

class StorageService:
    def __init__(
            self,

    ) -> None:
        ...

    async def get_storages(self):
        ...

    async def get_storage_by_id(self, storage_id: int):
        ...

    async def create_storage(self):
        ...

    async def delete_storage(self):
        ...
