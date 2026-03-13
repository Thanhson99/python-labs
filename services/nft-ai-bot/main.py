import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
STABLE_DIFFUSION_API = "https://stablediffusionapi.com/api/v3/text2img"

print(GEMINI_API_KEY)

def generate_image_prompt(user_input):
    """
    Generate an image description using Gemini AI.
    :param user_input: Text input describing the type of image
    :return: Generated prompt
    """
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key={GEMINI_API_KEY}",
        headers={"Content-Type": "application/json"},
        json={"prompt": {"text": f"Generate a detailed artistic description for an NFT image about: {user_input}"}}
    )
    
    data = response.json()
    if "candidates" not in data:
        print("Error: Unexpected API response", data)
        return "A futuristic cyberpunk cat with neon lights."
    
    return data["candidates"][0]["output"].strip()

def generate_nft_image(prompt, output_path="output.png"):
    """
    Generate an image using Stable Diffusion API.
    :param prompt: Text description for the AI-generated image
    :param output_path: File path to save the generated image
    :return: Path to the saved image
    """
    response = requests.post(STABLE_DIFFUSION_API, json={
        "key": os.getenv("STABLE_DIFFUSION_KEY"),
        "prompt": prompt,
        "width": 512,
        "height": 512,
        "samples": 1
    })
    
    data = response.json()
    if "output" not in data or not data["output"]:
        print("Error: Failed to generate image", data)
        return None
    
    image_url = data["output"][0]
    image_data = requests.get(image_url).content
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path

def main():
    user_input = input("Enter a concept for your NFT: ")
    prompt = generate_image_prompt(user_input)
    print(f"Generated Prompt: {prompt}")
    image_path = generate_nft_image(prompt)
    if image_path:
        print(f"NFT Image saved at: {image_path}")
    else:
        print("Failed to generate image.")

if __name__ == "__main__":
    main()
