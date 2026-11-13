from typing import Iterator, Any

from .entity import Entity


class World:
    """
    ECS storage simples: dict[type_componente, dict[entity_id, componente]].
    Suficiente para milhares de entidades. Migrar para sparse set/SoA quando medir.
    """

    def __init__(self):
        self._next_id = 0
        self._free: list[int] = []
        self._components: dict[type, dict[int, Any]] = {}

    def create(self) -> Entity:
        if self._free:
            eid = self._free.pop()
        else:
            eid = self._next_id
            self._next_id += 1
        return Entity(eid)

    def destroy(self, e: Entity) -> None:
        for storage in self._components.values():
            storage.pop(e.id, None)
        self._free.append(e.id)

    def add(self, e: Entity, component: Any) -> None:
        self._components.setdefault(type(component), {})[e.id] = component

    def remove(self, e: Entity, ctype: type) -> None:
        self._components.get(ctype, {}).pop(e.id, None)

    def get(self, e: Entity, ctype: type):
        return self._components.get(ctype, {}).get(e.id)

    def has(self, e: Entity, ctype: type) -> bool:
        return e.id in self._components.get(ctype, {})

    def query(self, *ctypes: type) -> Iterator[tuple[int, tuple]]:
        """
        Iter para entidades que possuem TODOS os componentes.
        Yields: (entity_id, (comp1, comp2, ...)).
        """
        if not ctypes:
            return
        storages = [self._components.get(t, {}) for t in ctypes]
        if not all(storages):
            return
        base = min(storages, key=len)
        for eid in base:
            if all(eid in s for s in storages):
                yield eid, tuple(s[eid] for s in storages)