import os
import json

def generate_manifest(directory_path):
    manifest_template = {
        "assetsLocation": "./mf-assets/",
        "format": "vrm",
        "traitsDirectory": "./models/",
        "thumbnailsDirectory": "./models/",
        "exportScale": 1,
        "animationPath": get_animation_paths(),
        "traitIconsDirectorySvg": "./mf-assets/icons/",
        "defaultCullingLayer": -1,
        "defaultCullingDistance": [0.1, 0.01],
        "initialTraits": ["Body", "Hoodie", "Pants", "Sneakers"], 
        "offset": [0.0, 0.48, 0.0],
        "traits": generate_traits(directory_path),
        "textureCollections": [],
        "colorCollections": []
    }

    return json.dumps(manifest_template, indent=2)

def get_animation_paths():
    animation_directory = "./animations"
    animation_paths = [os.path.join(animation_directory, file) for file in os.listdir(animation_directory) if file.endswith(".fbx")]
    return sorted(animation_paths)

def generate_traits(directory_path):
    traits = []

    trait_culling_layers = {
        "Body": 0,
        "Hoodie": 1,
        "Longsleeve": 1,
        "MiniT": 1,
        "Pants": 1,
        "Shorts_Long": 1,
        "Shorts_Short": 1,
        "Sneakers": 1,
        "Tanktop": 1,
        "Tshirt": 1,
        "Vest": 1
    }

    for trait_name, culling_layer in trait_culling_layers.items():
        trait = {
            "trait": trait_name,
            "name": trait_name.capitalize(),
            "icon": "",
            "type": "mesh",
            "iconGradient": "",
            "iconSvg": f"{trait_name.upper()}.svg",
            "cullingLayer": culling_layer,
            "cameraTarget": {"distance": 3.0, "height": 0.8},
            "cullingDistance": [0.1, 0.01],
            "collection": generate_collection(directory_path, trait_name)
        }

        traits.append(trait)

    return traits

def generate_collection(directory_path, trait_name):
    trait_directory_path = os.path.join(directory_path, trait_name)

    return [
        {
            "id": entry[:-4],
            "name": entry[:-4].replace("_", " "),
            "directory": f"{trait_name}/{entry}",
            "thumbnail": f"{trait_name}/t_{entry[:-4]}.png",
            "textureCollection": f"Texture {trait_name}",
        }
        for entry in os.listdir(trait_directory_path)
        if entry.endswith(".vrm")
    ]

#def append_texture_collection(manifest_template, trait_name, texture):
#    # Append texturecollections for each trait
#    texture_collection = {
#        "trait": f"Texture {trait_name}",
#        "type": "texture",
#        "collection": [
#            {
#                "id": f"{trait_name}",
#                "name": f"{trait_name}",
#                "directory": f"{trait_name}/{texture}.png",
#                "thumbnail": f"{trait_name}/{texture}.png"
#            }
#        ]
#    }
#    manifest_template["textureCollections"].append(texture_collection)

def append_texture_collection(manifest_template, trait_name, trait_directory):
    texture_collection = {
        "trait": f"Texture {trait_name}",
        "type": "texture",
        "collection": []
    }
    
    trait_directory_path = os.path.join("./models/", trait_directory)
    png_files = [file for file in os.listdir(trait_directory_path) if file.endswith(".png")]

    for idx, png_file in enumerate(png_files):
        texture_entry = {
            "id": f"{trait_name}_{idx}",
            "name": f"{trait_name}_{idx}",
            "directory": f"{trait_directory}/{png_file}",
            "thumbnail": f"{trait_directory}/{png_file}"
        }
        texture_collection["collection"].append(texture_entry)

    manifest_template["textureCollections"].append(texture_collection)

if __name__ == "__main__":
    directory_path = "./models/"
    manifest_content = generate_manifest(directory_path)

    manifest_template = json.loads(manifest_content)

    # Call append_texture_collection function for each trait
    for trait_name in ["Body", "Hoodie", "Longsleeve", "MiniT", "Pants", "Shorts_Long", "Shorts_Short", "Sneakers", "Tshirt", "Tanktop"]:
        append_texture_collection(manifest_template, trait_name, trait_name)

    updated_manifest_content = json.dumps(manifest_template, indent=2)

    with open("./models/manifest.json", "w") as manifest_file:
        manifest_file.write(updated_manifest_content)

    print("Manifest file generated successfully.")


#if __name__ == "__main__":
#    directory_path = "./models/"
#    manifest_content = generate_manifest(directory_path)
#
#    # Parse manifest_content string into a dictionary
#    manifest_template = json.loads(manifest_content)
#
#    # Call append_texture_collection function for each trait
#    for trait_name in ["Body", "Hoodie", "Longsleeve", "MiniT", "Pants", "Shorts_Long", "Shorts_Short", "Sneakers", "Tanktop", "Tshirt", "Vest"]:
#        append_texture_collection(manifest_template, trait_name, "your_texture_name_here")
#
#    # Convert manifest_template back to JSON string
#    updated_manifest_content = json.dumps(manifest_template, indent=2)
#
#    with open("./models/manifest.json", "w") as manifest_file:
#        manifest_file.write(updated_manifest_content)
#
#    print("Manifest file generated successfully.")

#if __name__ == "__main__":
#    directory_path = "./models/"
#    manifest_content = generate_manifest(directory_path)
#
#
#    with open("./models/manifest.json", "w") as manifest_file:
#        manifest_file.write(manifest_content)
#
#    print("Manifest file generated successfully.")
