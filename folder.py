"""Folder management functionality for Bitwarden to KeePass conversion.

Provides classes and functions for managing folder hierarchies when converting
from Bitwarden's folder structure to KeePass groups.
"""

import collections
from typing import Callable, Deque, List, Optional

from pykeepass.group import Group as KPGroup


class Folder:
    """Represents a folder in the Bitwarden/KeePass hierarchy.

    Attributes:
        id: Bitwarden folder identifier
        name: Display name of the folder
        children: List of child folders
        parent: Parent folder reference
        keepass_group: Associated KeePass group object
    """

    id: Optional[str]
    name: Optional[str]
    children: List["Folder"]
    parent: Optional["Folder"]
    keepass_group: Optional[KPGroup]

    def __init__(self, id_: Optional[str]):
        """Initialize a new folder.

        Args:
            folder_id: Bitwarden folder identifier
        """
        self.id = id_
        self.name = None
        self.children = []
        self.parent = None
        self.keepass_group = None

    def add_child(self, child: "Folder"):
        """Add a child folder to this folder.

        Args:
            child: Folder object to add as a child
        """
        self.children.append(child)
        child.parent = self


# logic was lifted directly from https://github.com/bitwarden/jslib/blob/ecdd08624f61ccff8128b7cb3241f39e664e1c7f/common/src/misc/serviceUtils.ts#L7
def nested_traverse_insert(root: Folder, name_parts: List[str], new_folder: Folder, delimiter: str) -> None:
    """Insert a new folder into the folder hierarchy.

    Args:
        root: Root folder to start traversal from
        name_parts: Path components for the new folder
        new_folder: Folder object to insert
        delimiter: Character used to separate path components
    """
    if len(name_parts) == 0:
        return

    end: bool = len(name_parts) == 1
    part_name: str = name_parts[0]

    for child in root.children:
        if child.name != part_name:
            continue

        if end and child.id != new_folder.id:
            # Another node with the same name.
            new_folder.name = part_name
            root.add_child(new_folder)
            return
        nested_traverse_insert(child, name_parts[1:], new_folder, delimiter)
        return

    if end:
        new_folder.name = part_name
        root.add_child(new_folder)
        return
    new_part_name: str = part_name + delimiter + name_parts[1]
    new_name_parts: List[str] = [new_part_name]
    new_name_parts.extend(name_parts[2:])
    nested_traverse_insert(root, new_name_parts, new_folder, delimiter)


def bfs_traverse_execute(root: Folder, callback: Callable[[Folder], None]) -> None:
    """Execute a callback on each folder in breadth-first order.

    Args:
        root: Root folder to start traversal from
        callback: Function to execute on each folder
    """
    queue: Deque[Folder] = collections.deque()
    queue.extend(root.children)
    while queue:
        child: Folder = queue.popleft()
        queue.extend(child.children)
        callback(child)
