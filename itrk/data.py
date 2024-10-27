# idea data in individual markdown files
# data/
#   idea1.md
#   idea2.md
#   idea3.md
#

# file format id using timestamp format YYMMDDhhmmss
# ---
# id: 241025154736
# title: "My First Idea"
# tags: ["python", "markdown", "storage"]
# status: tosser, inkling, ..., keeper 0, 1, ..., 5
# ---
#
# # My First Idea
#
# This is a description of the first idea.
# ...


import os
from datetime import datetime
from typing import List, Optional

import yaml


class Idea:
    def __init__(
        self, id: int, title: str, modified: int, tags: List[str], content: str
    ):
        self.id = id
        self.title = title
        self.modified = modified  # Replaces 'created' and tracks last modification
        self.tags = tags
        self.content = content

    @classmethod
    def from_markdown(cls, file_path: str):
        with open(file_path, "r") as file:
            content = file.read()
            metadata, content = content.split("---", 2)[1:]
            metadata = yaml.safe_load(metadata)

            return cls(
                id=int(metadata["id"]),
                title=metadata["title"],
                modified=int(metadata["modified"]),
                tags=metadata.get("tags", []),
                content=content.strip(),
            )

    def to_markdown(self) -> str:
        metadata = {
            "id": self.id,
            "title": self.title,
            "modified": self.modified,  # Store the modification timestamp
            "tags": self.tags,
        }
        yaml_metadata = yaml.dump(metadata, default_flow_style=False).strip()
        return f"---\n{yaml_metadata}\n---\n\n{self.content}"


class IdeaManager:
    def __init__(self, directory: str):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _get_idea_file_path(self, idea_id: int) -> str:
        return os.path.join(self.directory, f"idea{idea_id}.md")

    def generate_timestamp(self) -> int:
        # Generate a 12-digit timestamp in the format "yyMMddhhmmss"
        return int(datetime.now().strftime("%y%m%d%H%M%S"))

    def load_all_ideas(self) -> List[Idea]:
        ideas = []
        for file_name in os.listdir(self.directory):
            if file_name.endswith(".md"):
                file_path = os.path.join(self.directory, file_name)
                idea = Idea.from_markdown(file_path)
                ideas.append(idea)
        return ideas

    def load_idea_by_id(self, idea_id: int) -> Optional[Idea]:
        file_path = self._get_idea_file_path(idea_id)
        if os.path.exists(file_path):
            return Idea.from_markdown(file_path)
        return None

    def save_idea(self, idea: Idea):
        file_path = self._get_idea_file_path(idea.id)
        with open(file_path, "w") as file:
            file.write(idea.to_markdown())

    def create_new_idea(self, title: str, tags: List[str], content: str) -> Idea:
        # Use the generate_timestamp method from the manager to create a unique ID
        new_id = self.generate_timestamp()
        new_idea = Idea(
            id=new_id,
            title=title,
            modified=new_id,  # Initialize modified to be the same as the id
            tags=tags,
            content=content,
        )
        self.save_idea(new_idea)
        return new_idea

    def update_idea(
        self,
        idea_id: int,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        content: Optional[str] = None,
    ) -> bool:
        idea = self.load_idea_by_id(idea_id)
        if idea:
            if title:
                idea.title = title
            if tags is not None:
                idea.tags = tags
            if content:
                idea.content = content
            # Update the 'modified' timestamp using the manager's generate_timestamp
            idea.modified = self.generate_timestamp()
            self.save_idea(idea)
            return True
        return False

    def delete_idea(self, idea_id: int) -> bool:
        file_path = self._get_idea_file_path(idea_id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
