

def code_to_image(code,filename,fileadress):
    #(background) blue
    line_sep = code.splitlines()
    color_elements={}
    color_name = []
    color_name_string = ""
    count_text_name = 0
    text_name = []
    text_name_string = ""
    text_name_text = []
    text_name_text_string = ""
    color_count_name = 0
    text_elements = {}
    color_element_name = []
    color_element_name_string = ""
    background_count_name = 0
    background_color_string = ""
    background_color_list = []
    b = 0
    for line in line_sep:
        b+=1
        lex_line = list(line)
        count_text_name = 0
        text_name = []
        text_name_string = ""
        text_name_text = []
        text_name_text_string = ""

        color_count_name = 0
        color_name = []
        color_name_string = ""
        color_element_name = []
        color_element_name_string = ""
        # look for text
        if lex_line[0] == "(":
            if lex_line[1] == "t":
                if lex_line[2] == "e":
                    if lex_line[3] == "x":
                        if lex_line[4] == "t":
                            if lex_line[5] == "(":
                                for textname in lex_line[6:]:
                                    if textname != ")":
                                        count_text_name +=1
                                    else:
                                        break

                                for textname in lex_line[6: 6 + count_text_name]:
                                    text_name.append(textname)

                                text_name_string = "".join(text_name)
                                if lex_line[5+(count_text_name+1)] == ")":
                                    if lex_line[5+(count_text_name+2)] == ")":

                                        for i in lex_line[5 + (count_text_name + 3):]:
                                            text_name_text.append(i)
                                        text_name_text_string = "".join(text_name_text)
                                        text_elements[text_name_string] = text_name_text_string
        #look for color
        if lex_line[0] == "(":
            if lex_line[1] == "c":
                if lex_line[2] == "o":
                    if lex_line[3] == "l":
                        if lex_line[4] == "o":
                            if lex_line[5] == "r":

                                if lex_line[6] == "(":
                                    for colorname in lex_line[6:]:
                                        if colorname != ")":
                                            color_count_name += 1
                                        else:
                                            break
                                    for i in lex_line[7: 6 + color_count_name]:
                                        color_name.append(i)
                                    color_name_string = "".join(color_name)

                                    if lex_line[6+(color_count_name)] == ")":
                                        if lex_line[6+(color_count_name+1)] == ")":
                                            if lex_line[6+(color_count_name+2)] != "":
                                                for j in lex_line[6+(color_count_name+2):]:
                                                    color_element_name.append(j)
                                                color_element_name_string = "".join(color_element_name)
                                                color_elements[color_name_string] = color_element_name_string
        #look for background: (background) blue \n : gives background a color
        if lex_line[0] == "(":
            if lex_line[1] == "b":
                if lex_line[2] == "a":
                    if lex_line[3] == "c":
                        if lex_line[4] == "k":
                            if lex_line[5] == "g":
                                if lex_line[6] == "r":
                                    if lex_line[7] == "o":
                                        if lex_line[8] == "u":
                                            if lex_line[9] == "n":
                                                if lex_line[10] == "d":
                                                    if lex_line[11] == ")":
                                                        if lex_line[12] == " ":

                                                            # Just grab everything from index 13 to the end!
                                                            background_color_list = []
                                                            for i in lex_line[13:]:
                                                                background_color_list.append(i)

                                                            background_color_string = "".join(background_color_list).strip()
        else:
            background_color_string = ""

    payload = {
        "background": background_color_string,
        "text": text_elements,
        "color": color_elements
    }
    import os
    from PIL import Image, ImageDraw, ImageFont

    # --- Canvas Initialization ---
    canvas_width = 1920
    canvas_height = 1080

    bg_color = payload["background"] if payload["background"] != "" else "white"
    img = Image.new("RGB", (canvas_width, canvas_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 45)
    except IOError:
        font = ImageFont.load_default()

    # --- Layout Grid Coordinates Tracking ---
    start_x = 60  # Left margin padding
    start_y = 60  # Top margin padding
    current_x = start_x
    current_y = start_y

    column_width = 500  # Horizontal space allocated for each text column
    line_spacing = 25  # Vertical space between blocks of text

    # --- Loop Through Text Key-Value Pairs ---
    for key_id, text_content in payload["text"].items():

        # Safely grab the color using the same key_id (e.g., "start_text")
        # If a key doesn't have an explicit color, it defaults to white
        text_color = payload["color"].get(key_id, "white")

        # Calculate text dimensions for accurate boundary wrapping
        text_bbox = font.getbbox(text_content)
        text_height = text_bbox[3] - text_bbox[1]

        # TOP-TO-BOTTOM Boundary Check:
        # If the text height exceeds our bottom padding limit (1080 - 60)
        if current_y + text_height > (canvas_height - 60):
            current_x += column_width  # Move one column to the right
            current_y = start_y  # Reset back to the top of the canvas

        # LEFT-TO-RIGHT Safety Check:
        # Stop drawing if we run completely off the right edge of the screen
        if current_x > (canvas_width - 60):
            print("Warning: Out of canvas screen space!")
            break

        # Paint the string onto the image using its paired color
        # Change this line in your main.py (line 153):
        draw.text((current_x, current_y), text_content, fill=text_color.strip(), font=font)
        # Move the cursor down for the next line element
        current_y += text_height + line_spacing

    # --- Save Final File ---
    current_dir = fileadress
    img.save(os.path.join(current_dir, filename))


