import json
import os
import shutil
from typing import Any, Dict, List, Optional, Callable, Union
from datetime import datetime
import uuid


class JsonCRUD:
    """
    JSON CRUD utility for handling arrays of items in JSON files
    Similar to database table operations
    """

    def __init__(self, file_path: str, auto_backup: bool = True):
        """
        Initialize JSON CRUD handler

        Args:
            file_path: Path to the JSON file
            auto_backup: Whether to create backups before modifications
        """
        self.file_path = file_path
        self.auto_backup = auto_backup
        self.backup_dir = os.path.join(os.path.dirname(file_path), 'backups')

        # Ensure file exists
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create file with empty array if it doesn't exist"""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self._save_data([])

    def _load_data(self) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON file must contain an array")
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: List[Dict[str, Any]]):
        """Save data to JSON file"""
        if self.auto_backup:
            self._create_backup()

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def _create_backup(self):
        """Create backup of current file"""
        if os.path.exists(self.file_path):
            os.makedirs(self.backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(
                self.backup_dir,
                f"{os.path.basename(self.file_path)}.{timestamp}.bak"
            )
            shutil.copy2(self.file_path, backup_path)

    def _generate_id(self) -> str:
        """Generate unique ID"""
        return str(uuid.uuid4())

    def _find_index(self, condition: Union[Dict, Callable]) -> int:
        """Find index of first item matching condition"""
        data = self._load_data()

        for i, item in enumerate(data):
            if callable(condition):
                if condition(item):
                    return i
            elif isinstance(condition, dict):
                if all(item.get(k) == v for k, v in condition.items()):
                    return i
        return -1

    # CREATE operations
    def create(self, item: Dict[str, Any], auto_id: bool = True) -> Dict[str, Any]:
        """
        Create a new item

        Args:
            item: Item to create
            auto_id: Whether to auto-generate an ID

        Returns:
            Created item with ID
        """
        data = self._load_data()

        if auto_id and 'id' not in item:
            item['id'] = self._generate_id()

        item['created_at'] = datetime.now().isoformat()
        item['updated_at'] = datetime.now().isoformat()

        data.append(item)
        self._save_data(data)

        return item

    def create_many(self, items: List[Dict[str, Any]], auto_id: bool = True) -> List[Dict[str, Any]]:
        """Create multiple items"""
        data = self._load_data()
        created_items = []

        for item in items:
            if auto_id and 'id' not in item:
                item['id'] = self._generate_id()

            item['created_at'] = datetime.now().isoformat()
            item['updated_at'] = datetime.now().isoformat()

            data.append(item)
            created_items.append(item)

        self._save_data(data)
        return created_items

    # READ operations
    def read_all(self) -> List[Dict[str, Any]]:
        """Read all items"""
        return self._load_data()

    def read_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Read item by ID"""
        data = self._load_data()
        for item in data:
            if item.get('id') == item_id:
                return item
        return None

    def find(self, condition: Union[Dict, Callable]) -> List[Dict[str, Any]]:
        """
        Find items matching condition

        Args:
            condition: Dict with key-value pairs or callable function

        Returns:
            List of matching items
        """
        data = self._load_data()
        results = []

        for item in data:
            if callable(condition):
                if condition(item):
                    results.append(item)
            elif isinstance(condition, dict):
                if all(item.get(k) == v for k, v in condition.items()):
                    results.append(item)

        return results

    def find_one(self, condition: Union[Dict, Callable]) -> Optional[Dict[str, Any]]:
        """Find first item matching condition"""
        results = self.find(condition)
        return results[0] if results else None

    def paginate(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Paginate results"""
        data = self._load_data()
        total = len(data)
        start = (page - 1) * per_page
        end = start + per_page

        return {
            'data': data[start:end],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }

    # UPDATE operations
    def update_by_id(self, item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update item by ID"""
        data = self._load_data()

        for i, item in enumerate(data):
            if item.get('id') == item_id:
                data[i].update(updates)
                data[i]['updated_at'] = datetime.now().isoformat()
                self._save_data(data)
                return data[i]

        return None

    def update_many(self, condition: Union[Dict, Callable], updates: Dict[str, Any]) -> int:
        """Update multiple items matching condition"""
        data = self._load_data()
        updated_count = 0

        for i, item in enumerate(data):
            match = False
            if callable(condition):
                match = condition(item)
            elif isinstance(condition, dict):
                match = all(item.get(k) == v for k, v in condition.items())

            if match:
                data[i].update(updates)
                data[i]['updated_at'] = datetime.now().isoformat()
                updated_count += 1

        if updated_count > 0:
            self._save_data(data)

        return updated_count

    def upsert(self, condition: Union[Dict, Callable], item: Dict[str, Any]) -> Dict[str, Any]:
        """Update if exists, create if not"""
        existing = self.find_one(condition)

        if existing:
            item_id = existing.get('id')
            if item_id:
                return self.update_by_id(item_id, item)

        return self.create(item)

    # DELETE operations
    def delete_by_id(self, item_id: str) -> bool:
        """Delete item by ID"""
        data = self._load_data()

        for i, item in enumerate(data):
            if item.get('id') == item_id:
                del data[i]
                self._save_data(data)
                return True

        return False

    def delete_many(self, condition: Union[Dict, Callable]) -> int:
        """Delete multiple items matching condition"""
        data = self._load_data()
        original_count = len(data)

        data[:] = [
            item for item in data
            if not (
                condition(item) if callable(condition)
                else all(item.get(k) == v for k, v in condition.items())
            )
        ]

        deleted_count = original_count - len(data)

        if deleted_count > 0:
            self._save_data(data)

        return deleted_count

    def clear_all(self) -> int:
        """Delete all items"""
        data = self._load_data()
        count = len(data)
        self._save_data([])
        return count

    # UTILITY operations
    def count(self, condition: Union[Dict, Callable] = None) -> int:
        """Count items matching condition"""
        if condition is None:
            return len(self._load_data())
        return len(self.find(condition))

    def exists(self, condition: Union[Dict, Callable]) -> bool:
        """Check if item exists"""
        return self.find_one(condition) is not None

    def get_schema(self) -> Dict[str, set]:
        """Get schema information from existing data"""
        data = self._load_data()
        schema = {}

        for item in data:
            for key, value in item.items():
                if key not in schema:
                    schema[key] = set()
                schema[key].add(type(value).__name__)

        return {k: list(v) for k, v in schema.items()}

    def backup_now(self) -> str:
        """Create manual backup"""
        self._create_backup()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(
            self.backup_dir,
            f"{os.path.basename(self.file_path)}.{timestamp}.bak"
        )

    def restore_from_backup(self, backup_file: str):
        """Restore from backup file"""
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, self.file_path)
        else:
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
