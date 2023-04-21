import os
import zipfile
import xml.etree.ElementTree as ET

# Get the path to the directory where the Python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# loop through all files in the directory
for r, d, f in os.walk(script_dir):
    for file in f:
        # check if the file is a .cbz file  
        if file.endswith(".cbz"):

            # Join the script directory and the .cbz filename to create the full path to the .cbz file 
            cbz_path = os.path.join(r, file)  

            # Create a temporary archive to write the modified files
            temp_cbz_path = os.path.join(r, "temp.cbz")

            # Open the .cbz file using zipfile module
            with zipfile.ZipFile(cbz_path, "r") as cbz_file:

                # Extract the ComicInfo.xml file from the archive
                xml_data = cbz_file.read("ComicInfo.xml")

                # Parse the XML data using ElementTree module
                root = ET.fromstring(xml_data)

                # Find the element in the XML tree that contains the HTML-encoded data
                html_element = root.find(".//Summary")

                # Check if the data inside the HTML-encoded element is already enclosed with CDATA tags
                if not html_element.text.startswith("<![CDATA["):
                    # If not, add CDATA tags around the data
                    html_element.text = "<![CDATA[" + html_element.text + "]]>"
                
                # Decode the HTML-encoded data using the html module's unescape() function
                # decoded_data = html.unescape(html_element.text)
                decoded_data = html_element.text

                # Replace newline characters with <br /> HTML tags
                decoded_data = decoded_data.replace("\n", "<br />")
                
                # Update the HTML-encoded element with the formatted data
                html_element.text = decoded_data

                # Write the modified XML data to a temporary file in memory
                # Use ElementTree's write method with method="xml" to serialize the XML data as plain text 
                # (instead of using the default method="html")
                temp_xml_data = ET.tostring(root, encoding="unicode", xml_declaration=True)

                #replace html encoded &lt; into < in temp_xml_data string
                temp_xml_data = temp_xml_data.replace("&lt;", "<")
                #replace html encoded &gt; into > in temp_xml_data string
                temp_xml_data = temp_xml_data.replace("&gt;", ">")

                # Create a new temporary archive to write the modified files
                with zipfile.ZipFile(temp_cbz_path, "w") as temp_cbz_file:
        
                    # Iterate over all files in the original archive
                    for name in cbz_file.namelist():
                        
                        # Skip the ComicInfo.xml file
                        if name == "ComicInfo.xml":
                            continue
                        
                        # Read the content of the file from the original archive
                        file_content = cbz_file.read(name)
                        
                        # Write the content of the file to the new temporary archive
                        temp_cbz_file.writestr(name, file_content)
                    
                    # Write the modified XML data to the new temporary archive
                    temp_cbz_file.writestr("ComicInfo.xml", temp_xml_data)

            # Delete the original archive
            os.remove(cbz_path)

            # Rename the temporary archive to the original filename
            os.rename(temp_cbz_path, cbz_path)

            # Print a success message
            print(f"Formatted data saved to {file}")