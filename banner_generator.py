import json
import os
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
client = OpenAI(api_key="your-api-key")

def create_banner_from_json(json_data):
    # Parse JSON input
    data = json_data

    # Load the background image
    background_path = f"static/backgrounds/{data['background_image']}"
    background = Image.open(background_path)

    # Load the logos
    logos = []
    for logo_data in data.get("logos", []):
        logo_path = f"static/logos/{logo_data['logo_name']}"
        logos.append(Image.open(logo_path).convert("RGBA"))

    # Extract other inputs
    include_and_more = data.get("include_and_more", False)
    primary_copy = data.get("primary_copy", "")
    sub_copy = data.get("sub_copy", "")
    strike_through_text = data.get("strike_through", "")

    # Resize the background to a standard banner size
    banner_size = (800, 400)
    background = background.resize(banner_size)

    # Create a canvas matching the resized background image size
    canvas = Image.new('RGB', banner_size)

    # Paste the resized background onto the canvas
    canvas.paste(background, (0, 0))

    # Create a white box at the specified location
    offset_y = -30
    white_box_position = (150, 240 + offset_y, 650, 310 + offset_y)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(white_box_position, fill="white")

    # Resize and paste the logos
    logo_size = (100, 50)
    if include_and_more:
        total_width = len(logos) * logo_size[0] + 40  # Add space for "& More"
    else:
        total_width = len(logos) * logo_size[0] + (len(logos) - 1) * 20

    start_x = (banner_size[0] - total_width) // 2

    for i, logo in enumerate(logos):
        resized_logo = logo.resize(logo_size)
        canvas.paste(resized_logo, (start_x + i * (logo_size[0] + 20), 250 + offset_y), resized_logo)

    if include_and_more:
        # Add the "& More" as a third logo by creating a text image
        font_logo = ImageFont.truetype("/Library/Fonts/Arial.ttf", 24)
        and_more_image = Image.new('RGBA', logo_size, (255, 255, 255, 0))
        draw_logo = ImageDraw.Draw(and_more_image)
        text_bbox = draw_logo.textbbox((0, 0), "& More", font=font_logo)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        draw_logo.text(((logo_size[0] - text_w) // 2, (logo_size[1] - text_h) // 2), "& More", font=font_logo, fill="black")
        canvas.paste(and_more_image, (start_x + len(logos) * (logo_size[0] + 20), 250 + offset_y), and_more_image)

    # Center-align the main copy text below the logos
    font_large = ImageFont.truetype("/Library/Fonts/Arial.ttf", 28)
    text_bbox = draw.textbbox((0, 0), primary_copy, font=font_large)
    text_w = text_bbox[2] - text_bbox[0]
    draw.text(((banner_size[0] - text_w) // 2, 320 + offset_y), primary_copy, font=font_large, fill="white")

    # Center-align the sub copy text with strike-through if needed
    font_bold = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", 36)

    if strike_through_text:
        sub_copy_parts = sub_copy.split(strike_through_text)
        text_start_x = (banner_size[0] - draw.textbbox((0, 0), sub_copy, font=font_bold)[2]) // 2

        # Draw text before strike-through
        draw.text((text_start_x, 350 + offset_y), sub_copy_parts[0], font=font_bold, fill="white")
        current_x = text_start_x + draw.textbbox((0, 0), sub_copy_parts[0], font=font_bold)[2]

        # Draw strike-through text
        strike_text_bbox = draw.textbbox((current_x, 350 + offset_y), strike_through_text, font=font_bold)
        draw.text((current_x, 350 + offset_y), strike_through_text, font=font_bold, fill="white")
        strike_y = strike_text_bbox[1] + (strike_text_bbox[3] - strike_text_bbox[1]) // 2
        draw.line((strike_text_bbox[0], strike_y, strike_text_bbox[2], strike_y), fill="white", width=4)

        # Draw text after strike-through
        current_x += strike_text_bbox[2] - strike_text_bbox[0]
        draw.text((current_x, 350 + offset_y), sub_copy_parts[1], font=font_bold, fill="white")

    else:
        # If no strike-through, just draw the text
        text_start_x = (banner_size[0] - draw.textbbox((0, 0), sub_copy, font=font_bold)[2]) // 2
        draw.text((text_start_x, 350 + offset_y), sub_copy, font=font_bold, fill="white")

    # Save the final banner
    output_path = "static/final_banner.jpg"
    canvas.save(output_path)
    print(f"Banner created and saved as '{output_path}'")
    return output_path

def update_json_with_gpt(command, json_data):
    # List available backgrounds and logos
    available_backgrounds = os.listdir("static/backgrounds")
    available_logos = os.listdir("static/logos")
    
    # Provide GPT with the JSON structure and the command
    prompt = f"""
    The following is a JSON data structure for creating a banner:
    {json.dumps(json_data, indent=2)}
    
    The user has provided a command. The user may refer to the files in the directories approximately.
    
    Here is a list of available background images:
    {available_backgrounds}
    
    Here is a list of available logos:
    {available_logos}
    
    Please update the JSON structure accordingly based on the user's command and map approximate names to the best-matching file names. Don't change the schema. Just share json.
    """

    # Call the OpenAI API with the prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" or "gpt-4" if available
        max_tokens=2000,
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": command}
        ]
    )
    
    # Extract the generated JSON from the response
    updated_json = response.choices[0].message.content.strip()

    # Update the global json_data with the new data
    try:
        json_data = json.loads(updated_json)
        print("JSON updated successfully:")
        return json_data
    except json.JSONDecodeError as e:
        print("Error decoding JSON from GPT response:")
        print(e)
        print("GPT response was:")
        print(updated_json)
        return json_data
        