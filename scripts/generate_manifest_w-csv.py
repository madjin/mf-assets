import argparse
import csv
import json
import os

# Define the culling layer mapping
# -1 = always show
# 0 = usually body / skin
# 1 = will cull with 0 (so usually clothing)
# 2 = will cull with 0 and 1 (so usually hair)
# etc..
culling_layer_mapping = {
    "Body": 0,
    "Brace": 0,
    "Clips and Kanzashi": -1,
    "Clothing": 1,
    "Earring": -1,
    "Face Other": -1,
    "Glasses": -1,
    "Hair": 1,
    "Hair Accessory Other": -1,
    "Halos": -1,
    "Hats": -1,
    "Head": -1,
    "Head Accessory Other": -1,
    "Masks": -1,
    "Neck": -1,
    "Ribbons and Bows": -1,
    "Sigil": -1,
    "Tail": -1,
    "Weapon": -1,
    "Weapon Brace": -1,
    "Wings": -1
}

def read_csv_mapping(csv_file_path):
    id_mapping = {}

    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            original_name = row['Original']
            renamed_name = row['Rename']

            id_mapping[original_name] = renamed_name

    return id_mapping

def get_animation_paths(directory_path):
    animation_directory = os.path.join(directory_path, "_animations")
    animation_paths = [os.path.join("./anata-vrm/_animations", file) for file in os.listdir(animation_directory) if file.endswith(".fbx")]
    return sorted(animation_paths)


def get_id_from_mapping(trait_name, id_mapping):
    # Get the original name directly using trait_name
    renamed_name = id_mapping.get(trait_name, None)

    return renamed_name if renamed_name is not None else trait_name

def create_manifest(input_file, csv_file, id_mapping):
    """
    Generate a *_manifest.json file based on a given *_attributes.json file and a CSV file.

    Args:
        input_file (str): The input JSON file (*_attributes.json).
        csv_file (str): The input CSV file.

    This script takes an input JSON file (*_attributes.json) and a CSV file and generates a corresponding
    *_manifest.json file with specific formatting. It maps trait types to culling layers
    based on the culling_layer_mapping and creates the manifest accordingly.
    """

    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        name_mapping = {row['Original']: row['Rename'] for row in csv_reader}

    folder_name = data["name"]
    output_file = f"{folder_name}_manifest.json"

    # Define the template for the manifest
    manifest = {
        "thumbnail": f"./anata-vrm/_thumbnails/t_{folder_name}.jpg",
        "format": "vrm",
        "traitsDirectory": f"./anata-vrm/male/",
        "thumbnailsDirectory": f"./anata-vrm/male/",
        "exportScale": 0.7,
        "animationPath": get_animation_paths(directory_path),
        "traitIconsDirectorySvg": "./assets/_icons/",
        "requiredTraits": ["Body"],
        "defaultCullingLayer": -1,
        "defaultCullingDistance": [0.3, 0.3],
        "offset": [0, 0.48, 0],
        "initialTraits": ["Body", "Hair", "Clothing", "Head", "Face Other", "Clips and Kanzashi", "Neck", "Masks", "Glasses", "Hats", "Head Accessory Other", "Hair Accessory Other", "Ribbons and Bows", "Earring", "Wings", "Halos", "Tail"],
        "traits": [],
        "textureCollections": []
    }

    for attribute in data["attributes"]:
        trait_type = attribute["trait_type"]
        trait_value = attribute["value"]
        original_name = attribute.get("Original")  # Get the "Original" name from the attribute
        renamed_name = attribute.get("Rename")

        # Use the original name if available in the CSV mapping, otherwise use the trait_value
        display_name = name_mapping.get(original_name, trait_value)

        trait_entry = {
            "trait": trait_type,
            "name": trait_type.capitalize(),
            "icon": "",
            "type": "mesh",
            "iconGradient": "",
            "iconSvg": f"{trait_type.upper()}.svg",
            "cullingLayer": culling_layer_mapping.get(trait_type, -1),
            "cameraTarget": {"distance": 5, "height": 1.2},
            "cullingDistance": [0.03, 0.03] if trait_type =="Body" else [0.3, 0.3],
            "collection": [
                {
                    "id": trait_value,
                    "name": trait_value,
                    "directory": "BODY/male.vrm" if trait_type == "Body" else f"{folder_name}/{get_id_from_mapping(renamed_name or trait_value, id_mapping)}.vrm",
                    "thumbnail": "BODY/male.png" if trait_type == "Body" else f"{folder_name}/thumbnails/{get_id_from_mapping(renamed_name or trait_value, id_mapping)}.png",
                    "textureCollection": "Body Skin" if trait_type == "Body" else ""
                }
            ]
        }

        manifest["traits"].append(trait_entry)

    # Append textureCollections for "BODY" trait
    body_collection = {
        "trait": "Body Skin",
        "collection": [
            {
                "id": f"skin_{folder_name}",
                "name": f"Eyes {folder_name}",
                "directory": f"{folder_name}/skin_{folder_name}.png",
                "thumbnail": f"{folder_name}/skin_{folder_name}.png"
            }
        ]
    }
    manifest["textureCollections"].append(body_collection)

    with open(output_file, 'w') as output:
        json.dump(manifest, output, indent=2)

if __name__ == '__main__':
    directory_path = "/home/jin/repo/anata-vrm/"
    parser = argparse.ArgumentParser(description="Generate *_manifest.json file from *_attributes.json files")
    parser.add_argument("input_file", help="Input JSON file (*_attributes.json)")
    parser.add_argument("csv_file", help="Input CSV file with name mapping")
    args = parser.parse_args()
    id_mapping = read_csv_mapping(args.csv_file)

    create_manifest(args.input_file, args.csv_file, id_mapping)  # Include id_mapping argument
