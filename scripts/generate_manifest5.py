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
    "Hoodie": -1, 
    "Longsleeve": -1,
    "MiniT": -1,
    "Pants": -1,
    "Shorts_Long": -1,
    "Shorts_Short": -1,
    "Sneakers": -1,
    "Tanktop": -1,
    "Tshirt": -1,
    "Vest": -1
}


def get_animation_paths(directory_path):
    animation_directory = os.path.join(directory_path, "animations")
    animation_paths = [os.path.join("./mf-assets/animations", file) for file in os.listdir(animation_directory) if file.endswith(".fbx")]
    return sorted(animation_paths)

def get_id_from_mapping(trait_name, id_mapping):
    # Get the original name directly using trait_name
    renamed_name = id_mapping.get(trait_name, None)

    return renamed_name if renamed_name is not None else trait_name

def create_manifest(input_file, csv_file, id_mapping):
    output_file = f"manifest.json"

    # Define the template for the manifest
    manifest = {
        #"thumbnail": f"./mf-assets/_thumbnails/t_{folder_name}.jpg",
        "format": "vrm",
        "traitsDirectory": f"./mf-assets/models/",
        "thumbnailsDirectory": f"./mf-assets/models/",
        "exportScale": 0.7,
        "animationPath": get_animation_paths(directory_path),
        "traitIconsDirectorySvg": "./assets/_icons/",
        "requiredTraits": ["Body"],
        "defaultCullingLayer": -1,
        "defaultCullingDistance": [0.3, 0.3],
        "offset": [0, 0.48, 0],
        "initialTraits": ["Body", "Head", "Hand", "Foot", "Chest", "Waist", "Neck"],
        "traits": [],
        "textureCollections": []
    }

    for attribute in data["attributes"]:
        trait_type = attribute["trait_type"]
        trait_value = attribute["value"]
        #original_name = attribute.get("Original")  # Get the "Original" name from the attribute
        #renamed_name = attribute.get("Rename")

        # Use the original name if available in the CSV mapping, otherwise use the trait_value
        #display_name = name_mapping.get(original_name, trait_value)

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
                    "directory": "Body/hyperbot.vrm" if trait_type == "Body" else f"{folder_name}/{get_id_from_mapping(renamed_name or trait_value, id_mapping)}.vrm",
                    "thumbnail": "Body/hyperbot.png" if trait_type == "Body" else f"{folder_name}/thumbnails/{get_id_from_mapping(renamed_name or trait_value, id_mapping)}.png",
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
    directory_path = "/home/jin/repo/loot-vrm/"
    parser = argparse.ArgumentParser(description="Generate *_manifest.json file from *_attributes.json files")
    parser.add_argument("input_file", help="Input JSON file (*_attributes.json)")
    parser.add_argument("csv_file", help="Input CSV file with name mapping")
    args = parser.parse_args()
    id_mapping = read_csv_mapping(args.csv_file)

    create_manifest(args.input_file, args.csv_file, id_mapping)  # Include id_mapping argument
