import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Dulan Lokugeegana\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def get_total(input_image):
    # this function tries to return the total value as it is the only value missing
    # but this function is in development yet
    # for this code this function is not considered
    image = cv2.imread('bill.jpg')
    height, width, _ = image.shape
    split_height = height // 2  # Dividing the height in half
    upper_part = image[:split_height, :]
    lower_part = image[split_height:, :]
    cv2.imwrite('upper_part.jpg', upper_part)
    cv2.imwrite('lower_part.jpg', lower_part)
    # cv2.imshow('upper_part', upper_part)
    # cv2.imshow('lower_part', lower_part)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    final_text = extract_text('lower_part.jpg')

    last_numeric_value = 0
    # Iterate through the list
    for item in final_text.split(" ")[len(final_text.split(" "))-2: len(final_text.split(" "))]:
        # Attempt to convert the item to a float (numeric value)
        # print(item)
        try:
            numeric_value = float(item)
        except ValueError:
            pass
        if numeric_value > 0:
                last_numeric_value = numeric_value
    # print(last_numeric_value)
    return last_numeric_value

def show_img(input_image):
    input_image = cv.imread('bill.jpg')
    input_image = cv.cvtColor(input_image, cv.COLOR_BGR2RGB)
    plt.imshow(input_image, cmap='gray')
    plt.show()
    return None

def extract_text(input_image):
    bill_image = Image.open(input_image)
    text = pytesseract.image_to_string(bill_image)
    return text

def creating_the_dictionary(text):
    keys = ['Table', 'OR#', 'Date', 'Time', 'Staff', 'Cover', 'Consumed items', 'Total']

    found = [False]*len(keys)
    for i in range(len(keys)):
        if keys[i] in text:
            found[i] = True
    #print(found)

    values= []
    for i in range(len(keys)):
        # finding the length of the value if not found
        backuplen = 2
        if keys[i] == 'Table':
            backuplen = 4
        elif keys[i] == 'OR#':
            backuplen = 11
        elif keys[i] == 'Date':
            backuplen = 9
        elif keys[i] == 'Time':
            backuplen = 5
        elif keys[i] == 'Staff':
            backuplen = 7
        elif keys[i] == 'Cover':
            backuplen = 2
        elif keys[i] == 'Total':
            backuplen = 6

        if i == len(keys)-1:
            values.append(text[text.find(keys[i])+len(keys[i])+2 : backuplen + text.find(keys[i])+len(keys[i])])
        elif keys[i] == 'Date' or keys[i] == 'Time':
            values.append(text[text.find(keys[i])+len(keys[i])+4 : backuplen + text.find(keys[i])+len(keys[i])+4])
        else:
            if found[i] & found[i+1]:
                values.append(text[text.find(keys[i])+len(keys[i])+2 : text.find(keys[i+1])-1])
            elif not found[i]:
                values.append('Not Found')
            elif found[i] & ~found[i+1]:
                values.append(text[text.find(keys[i])+len(keys[i])+3 : backuplen + text.find(keys[i])+len(keys[i])+3])

    # Creating the item list

    cleaned_values = [element.strip() for element in values]
    # print(cleaned_values)
    dictionary = {}
    for i in range(len(keys)):
        dictionary[keys[i]] = cleaned_values[i]
    
    things1 = text[text.find('Cover') + len('Cover')+2 : text.find('MPH')-2]
    # print(things1)
    start_index = 0
    lines = things1.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == "Date":
            start_index = i
            break
    things = lines[start_index+2:]
    # print(things)

    item_list = []

    # Process each line and extract the item and price
    for line in things:
        parts = line.split()
        if len(parts) >= 3:
            item = ' '.join(parts[1:-1])
            price = parts[-1]
            item_list.append({"item": item, "price": price})

    # print(item_list)
    dictionary['Consumed items'] = item_list

    # the below function is yet to be developed
    # dictionary['Total'] = get_total('bill.jpg')
            
    return dictionary

def creatingJson(dictionary):
    json_data = json.dumps(dictionary)
    # print(json_data)
    return json_data



def main():
    image_data = extract_text('bill.jpg')
    dictionary = creating_the_dictionary(image_data)
    json_data = creatingJson(dictionary)
    # print(dictionary)
    print(json_data)
    return None

main()

