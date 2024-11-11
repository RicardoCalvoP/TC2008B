from PIL import Image, ImageDraw

def create_trash_image(output_filename="Poop_Emoji2.png"):
    """
    Creates a trash icon with a white 5px border and a trashier design on a gray background.
    """
    # Image size
    width, height = 120, 120  # Increased size for the border
    background_color = (128, 128, 128)  # Gray background
    trash_color = (255, 255, 255)  # White for the trash and border

    # Create the image with a background
    image = Image.new("RGB", (width, height), background_color)

    # Draw the white border
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, width - 1, height - 1], outline=trash_color, width=5)

    # Draw the trash can body
    trash_body_coords = [40, 30, 80, 90]
    draw.rectangle(trash_body_coords, fill=trash_color)

    # Add trash lines to make it "trashy"
    for x in range(45, 80, 7):  # Vertical lines inside the trash can
        draw.line([x, 35, x, 85], fill=background_color, width=2)

    # Draw the trash can lid
    trash_lid_coords = [35, 25, 85, 35]
    draw.rectangle(trash_lid_coords, fill=trash_color)

    # Add a handle on the lid
    handle_coords = [55, 20, 65, 25]
    draw.rectangle(handle_coords, fill=trash_color)

    # Save the image
    image.save(output_filename)
    print(f"Image saved as {output_filename}")

# Execute the function
if __name__ == "__main__":
    create_trash_image()
