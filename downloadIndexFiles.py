import os
import time
import requests  # To fetch the raw HTML content
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Step 1: Setup the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Function to download index.html file from a GitHub repository
def download_index_html(github_url):

    # Step 2: Open the GitHub repository page
    driver.get(github_url)
    
    # Give time for the page to load
    time.sleep(6)
    
    # Step 3: Check if the file index.html exists in the repository's root directory
    try:
        # Look for the index.html file in the repository
        index_file = driver.find_element(By.LINK_TEXT, 'index.html')
        
        # If index.html exists, click to open the file page
        index_file.click()
        
        # Wait for the file page to load
        time.sleep(4)
        
        # Step 4: Find and click the "Raw" button to go to the raw HTML content
        raw_button = driver.find_element(By.LINK_TEXT, 'Raw')
        raw_button.click()

        # Wait for the raw page to load
        time.sleep(4)
        
        # Step 5: Get the raw URL and download the content using requests
        raw_url = driver.current_url
        
        # Fetch the raw content using requests instead of Selenium to avoid escaping HTML tags
        response = requests.get(raw_url)
        if response.status_code == 200:
            raw_html_content = response.text
        else:
            print(f"Failed to fetch raw content. Status code: {response.status_code}")
            return
        
        # Step 6: Extract the course name from the raw URL (between "eo4geocourses" and "/refs")
        repo_name = raw_url.split("/")[4]  # "eo4geocourses" is at index 3, so repo name is at index 4
        
        # Step 7: Create the folder to store the index.html files if it doesn't exist
        if not os.path.exists("Index Files"):
            os.makedirs("Index Files")
        
        # Step 8: Save the raw HTML content using the extracted course name as the file name
        file_path = f"Index Files/{repo_name}_index.html"
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(raw_html_content)
        
        print(f"index.html downloaded and saved as: {file_path}")
    
    except Exception as e:
        print(f"index.html not found in the repository: {github_url}. Error: {str(e)}")

# List of GitHub repository URLs to go through
github_repos = [
   "https://github.com/eo4geocourses/PLUS_SciWri",
    "https://github.com/eo4geocourses/PLUS_OBIA",
    "https://github.com/eo4geocourses/PLUS_Copernicus-multilingual",
    "https://github.com/eo4geocourses/PLUS_OBIA-Introduction",
    "https://github.com/eo4geocourses/UNEP-GRID_EO-for-Urban-Greenery-Management",
    "https://github.com/eo4geocourses/UPAT_Air-quality-monitoring-and-management-webinar",
    "https://github.com/eo4geocourses/UPAT_Early_warning_for_disease_epidemics_at_regional_level",
    "https://github.com/eo4geocourses/GISIG_Introduction_to_EO4GEO",
    "https://github.com/eo4geocourses/GEOF_Understanding-the-concept-of-EO-time-series",
    "https://github.com/eo4geocourses/GEOF_Validation-of-EO-products",
    "https://github.com/eo4geocourses/GEOF_Preprocessing-of-EO-data",
    "https://github.com/eo4geocourses/UT-ITC_Satellite_Data_Classification_Random_Forests",
    "https://github.com/eo4geocourses/UT-ITC_Satellite_Data_Classification_Decision_Trees",
    "https://github.com/eo4geocourses/UNEP-GRID_Introduction-to-GIS",
    "https://github.com/eo4geocourses/KULeuven_Technical-Introduction-to-SDI",
    "https://github.com/eo4geocourses/KULeuven_Management-View-on-SDI",
    "https://github.com/eo4geocourses/UNIBAS_Remote-Sensing-Environment",
    "https://github.com/eo4geocourses/GEOF_Basic-GIS-knowledge-vector-and-raster-data",
    "https://github.com/eo4geocourses/FSU-Jena_SAR-Data-for-Flood-Mapping",
    "https://github.com/eo4geocourses/GEOF_Copernicus-Service-Land",
    "https://github.com/eo4geocourses/PLUS_DeepLearning",
    "https://github.com/eo4geocourses/Novogit_CO2_budgets",
    "https://github.com/eo4geocourses/UPAT_Solar_potential_maps_at_municipal_level",
    "https://github.com/eo4geocourses/SERCO_Active-fire-detection-with-Sentinel-3",
    "https://github.com/eo4geocourses/ClimateKIC-Spark_Earth_Observation_and_Geographic_Information",
    "https://github.com/eo4geocourses/UPAT_Air-quality-monitoring-and-management-workshop",
    "https://github.com/eo4geocourses/GIB_Evaluation_and_planning_of_urban_green_Infrastructures",
    "https://github.com/eo4geocourses/GIB_-Smart-cities-UHI-and-urban-green-technicalWorkshop",
    "https://github.com/eo4geocourses/GIB_-Smart-cities-UHI-and-urban-green-theoreticalWorkshop",
    "https://github.com/eo4geocourses/PLUS_EO_for_Landslide_Risk_Management",
    "https://github.com/eo4geocourses/PLANETEK_The_rise_of_Artificial_Intelligence_for_Earth_Observation",
    "https://github.com/eo4geocourses/ROSA_Change_detection_using_EO_data",
    "https://github.com/eo4geocourses/CNR-IREA_A-new-Common-Agricultural-Policy",
    "https://github.com/eo4geocourses/GEOF_EO-Data-sources",
    "https://github.com/eo4geocourses/IGIK_Sentinel2-Data-and-Vegetation-Indices",
    "https://github.com/eo4geocourses/IGIK_Introduction-to-Remote-Sensing",
    "https://github.com/eo4geocourses/EPSIT-GIB_Identification_of_heat_islands_to_support_city_planning",
    "https://github.com/eo4geocourses/ISPRA_Landslide_affecting_Cultural_Heritage_sites-Roman_Thermae_of_Baia",
    "https://github.com/eo4geocourses/GEOF_Fast-disaster-response",
    "https://github.com/eo4geocourses/IGEA_Usability_of_EO-IoT-GIS_data_in_agriculture",
    "https://github.com/eo4geocourses/PLUS_Practice-Image-Processing",
    "https://github.com/eo4geocourses/VITO_Parcel-Delineation",
    "https://github.com/eo4geocourses/UJI_AgroMonitoring-with-Geospatial-Data",
    "https://github.com/eo4geocourses/EPSIT-GIB_Identification_of_heat_islands_to_support_city_planning_recording",
    "https://github.com/eo4geocourses/UNEP-GRID_EO-for-Urban-Greenery-Management_Recording",
    "https://github.com/eo4geocourses/ClimateKIC_Copernicus-Service-Atmosphere",
    "https://github.com/eo4geocourses/IES_EO-for-Managers",
    "https://github.com/eo4geocourses/SpaSe_Urban-Heat-Islands",
    "https://github.com/eo4geocourses/UJI_Reproducible-Research-Practices-in-Geosciences",
    "https://github.com/eo4geocourses/ClimateKIC_Copernicus-Service-Climate-Change",
    "https://github.com/eo4geocourses/VITO_Data_Access_In_Terrascope",
    "https://github.com/eo4geocourses/UJI_Introduction-to-Programming",
    "https://github.com/eo4geocourses/ROSA_Change-Detection-in-optical-Data",
    "https://github.com/eo4geocourses/Novogit_Solar_Potential_Maps",
    "https://github.com/eo4geocourses/EO4GEO_RevealTemplate",
    "https://github.com/eo4geocourses/VITO_TerraScope_TrainingPack_Application_Example"
]

# Step 9: Iterate through the list of GitHub repositories
for repo in github_repos:
    download_index_html(repo)

# Close the WebDriver after processing all repositories
driver.quit()
