import json


def load_path(filename):
  with open(filename, 'r') as file:
    return json.load(file)

def get_registry_path(key):
  key = key.lower()
  return registry_paths.get(key, "key not found")


if __name__ == "__main__":
  hive = input("Enter loaded hive: ")
  registry_paths = load_path('paths.json')
  key = input("Enter the registry key: ")
  full_path = get_registry_path(key)
  print(f"Full registry path: {full_path}")
