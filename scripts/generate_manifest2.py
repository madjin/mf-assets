import os
import json

def get_animation_paths():
    animation_directory = "./animations"
    animation_paths = [os.path.join(animation_directory, file) for file in os.listdir(animation_directory) if file.endswith(".fbx")]
    return sorted(animation_paths)

def generate_traits(directory_path):
    traits = []

    trait_culling_layers = {
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
            "collection": generate_collection(directory_path, trait_name)  # Provide trait_name here
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

    # Append texturecollections for each trait
    texture_collection = {
        "trait": f"Texture {trait_name}",
        "type": "texture",
        "collection": [
            {
                "id": f"{trait_name}",
                "name": f"{trait_name}",
                "directory": f"{trait_name}/{texture}.png",
                "thumbnail": f"{trait_name}/{texture}.png"
            }
            for texture in os.listdir(trait_directory_path)
            if texture.endswith(".png")
        ]
    }
    manifest_template["textureCollections"].append(texture_collection)


if __name__ == "__main__":
    directory_path = "./models/"
    manifest_content = generate_traits(directory_path)  # Call generate_traits() instead

    with open("./models/manifest.json", "w") as manifest_file:
        manifest_file.write(json.dumps(manifest_content, indent=2))

    print("Manifest file generated successfully.")

