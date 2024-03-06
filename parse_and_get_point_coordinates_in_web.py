import xml.etree.ElementTree as ET
import requests

# Fetch the XML data from the URL
url = 'https://raw.githubusercontent.com/AzatSkyArchLab/ufa_urban_gov_data/main/MapPlan_08d6fdf2-ec9a-43ab-be7b-897b7bbe63bb.xml'
response = requests.get(url)
xml_data = response.content

# Parse the XML data
tree = ET.fromstring(xml_data)

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

# Write X and Y numbers to a text file
file_path = 'point_numbers.txt'
with open(file_path, 'w') as file:
    for data in point_data:
        file.write(f"X: {data['X']}, Y: {data['Y']}\n")

# Print a message to confirm the file creation
print(f"The X and Y numbers have been saved to {file_path}")
