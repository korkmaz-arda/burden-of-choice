import json


class MemoryFile:
    _instance = None
    path = None
    cache = []

    def __new__(cls, path=None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, path=None, *args, **kwargs):
        self.path = path if path is not None else "decision_memory.json"

    def load(self):
        try:
            with open(self.path, "r") as file:
                return MemoryResponse(data=data)
        except FileNotFoundError:
            msg = "Error: Unable to access memory file."
            return MemoryResponse(msg)
        except json.JSONDecodeError:
            msg = "Error: Invalid JSON format in the memory file."
            return MemoryResponse(msg)
        except Exception as e:
            msg = f"Error: An unexpected error occurred while loading memory: {e}"
            return MemoryResponse(msg)

    def save(self, data):
        cache.append(data.copy())
        try:
            with open(self.path, "w") as file:
                json.dump(data, file)
            return MemoryResponse()
        except Exception as e:
            msg = f"Error: An unexpected error occurred while saving memory: {e}"
            return MemoryResponse(msg)


class MemoryResponse:
    def __init__(self, error_message=None, data=None):
        self.error_message = error_message
        self.data = data