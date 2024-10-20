import os
import json
from bs4 import BeautifulSoup

# Define the folder containing the index.html files
folder_path = 'Index files'
# Define the path for the final JSON file outside the repository
final_json_file_path = 'Course_metadata.json'

# List to store metadata from all files
metadata_list = []

# Function to extract metadata from the <head> tag
def extract_metadata_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the entire file
        content = file.read()
        
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Dictionary to store metadata for this file
        metadata = {}

        # Find all <meta> and <link> tags within <head>
        head_tag = soup.find('head')
        if head_tag:
            # Process <meta> tags with property attributes starting with "dc:"
            meta_tags = head_tag.find_all('meta', property=True)
            for tag in meta_tags:
                property_attr = tag.get('property')
                if property_attr.startswith('dc:'):
                    # Special handling for dc:subject to split into an array
                    if property_attr == 'dc:subject':
                        metadata[property_attr[3:]] = [item.strip() for item in tag.get('content').split(',')]
                    elif property_attr in ['dc:creator', 'dc:contributor']:
                        # Split the content by commas and strip whitespace
                        creators = [name.strip() for name in tag.get('content').split(',')]
                        
                        # If the property already exists, extend the list
                        if property_attr[3:] in metadata:
                            metadata[property_attr[3:]].extend(creators)
                        else:
                            # Initialize with the creators list
                            metadata[property_attr[3:]] = creators
                    else:
                        # For other properties, just set the value
                        metadata[property_attr[3:]] = tag.get('content')

            # Process <link> tags with relation attributes starting with "dc:"
            link_tags = head_tag.find_all('link', rel=True)
            for tag in link_tags:
                relation_attr = tag.get('rel')[0]
                if relation_attr.startswith('dc:'):
                    # If the key already exists, append the new value to the list
                    if relation_attr[3:] in metadata:
                        # Ensure it's a list
                        if isinstance(metadata[relation_attr[3:]], list):
                            metadata[relation_attr[3:]].append(tag.get('href'))
                        else:
                            metadata[relation_attr[3:]] = [metadata[relation_attr], tag.get('href')]
                    else:
                        # Initialize with the href value
                        metadata[relation_attr[3:]] = [tag.get('href')]
        
        return metadata

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)
        # Extract metadata from the HTML file
        metadata = extract_metadata_from_html(file_path)
        
        # Append the metadata dictionary to the list
        metadata_list.append(metadata)

# Write all metadata to a single JSON file
with open(final_json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(metadata_list, json_file, indent=4, ensure_ascii=False)

print(f"All metadata extracted and saved to {final_json_file_path}")
