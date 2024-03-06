
import os
import zipfile
import xml.etree.ElementTree as ET


# Path to the zip file. Here just raw example of choosing directory
zip_file_path = 'C:/Users/Home/Downloads/Уфа Часть1/Ж3.16.zip'

# Directory to extract the file
extract_dir = 'C:/Users/Home/Downloads/Уфа Часть1/extracted_files'

# Ensure the extraction directory exists
os.makedirs(extract_dir, exist_ok=True)

# Extract the file with the 'MapPlan_' prefix from the zip archive
with zipfile.ZipFile(zip_file_path, 'r') as zipf:
    for file_info in zipf.infolist():
        if file_info.filename.startswith('MapPlan_'):
            zipf.extract(file_info, extract_dir)
            extracted_file_path = os.path.join(extract_dir, file_info.filename)
            break

# Fetch the XML data from the URL
file_list = os.listdir(extract_dir)
xml_file = next((file for file in file_list if file.endswith('.xml')), None)

if xml_file:
    xml_file_path = os.path.join(extract_dir, xml_file)
    print(f"The XML file '{xml_file}' is located at: {xml_file_path}")

    # Parse the XML data
    tree = ET.parse(xml_file_path)

    namespaces = {'Spa1': 'urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/1.0.2'}
    # Find all elements with the tag "Точка"
    point_elements = tree.findall('.//Spa1:SpatialElement', namespaces)

    # Extract X and Y numbers from each "Точка" element
    point_data = []
    for element in point_elements:
        for point in element.findall('.//Spa1:Ordinate', namespaces):
            x_number = point.get('X')
            y_number = point.get('Y')

            point_data.append({'X': x_number, 'Y': y_number})

    file_name = 'point_numbers.txt'
    # Full file path
    file_path = os.path.join(extract_dir, file_name)

    # Write X and Y numbers to the file
    with open(file_path, 'w') as file:
        for data in point_data:
            file.write(f"{data['X']}, {data['Y']}\n")

    # Print a message to confirm the file creation
    print(f"The X and Y numbers have been saved to {file_path}")
else:
    print("No XML file found in the directory.")

