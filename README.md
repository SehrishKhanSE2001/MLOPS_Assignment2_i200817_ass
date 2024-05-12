# MLOps Implementation with Apache Airflow

## Workflow Overview:

The workflow for this assignment consists of three major steps: Data Extraction, Data Transformation, and Data Storage and Version Controlling. These steps are orchestrated using Apache Airflow to automate the processes. Below is an overview of each step:

1. **Data Extraction:**
   - Utilized dawn.com and BBC.com as data sources.
   - Extracted links from the landing pages and titles with descriptions from articles displayed on their homepages.

2. **Data Transformation:**
   - Preprocessed the extracted text data by removing HTML tags, special characters, and converting text to lowercase for further analysis.

3. **Data Storage and Version Control:**
   - Stored the processed data on Google Drive for easy access and sharing.
   - Implemented Data Version Control (DVC) to track versions of the data. Metadata was versioned against each DVC push to the GitHub repository for traceability and reproducibility.
   - With these commands:
   -1. pip install dvc , 2. dvc init , 3. dvc remote add -d mydrive gdrive://<Google Drive folder ID> , 4. dvc add dawn_processed_data.txt bbc_processed_data.txt , 5. dvc push , 6. git add .dvc .gitignore dawn_processed_data.txt.dvc bbc_processed_data.txt.dvc git commit -m "Add processed data files and DVC metadata" git push origin master




4. **Apache Airflow DAG Development:**
   - Developed an Airflow DAG to automate the processes of extraction, transformation, and storage. Task dependencies and error management were handled effectively for a robust workflow.


## Documentation:

### Data Pre-processing Steps:
1. **Extracting Links and Article Information:**
   - Python scripts utilize BeautifulSoup and requests library to extract links and article details from dawn.com and BBC.com landing pages.

2. **Data Transformation:**
   - Text data preprocessing involves removing HTML tags, special characters, and converting text to lowercase for consistency.

3. **Storing Processed Data:**
   - Processed data is written to separate text files for Dawn and BBC articles (`dawn_processed_data.txt` and `bbc_processed_data.txt`).

### DVC (Data Version Control) Setup:
1. **Installation and Setup:**
   - DVC was installed and initialized in the project directory.
   
2. **Tracking Data:**
   - Processed data files were added to DVC control using `dvc add`, and changes were committed to the local repository.
   
3. **Pushing to GitHub Repository:**
   - Changes were pushed to the GitHub repository, and data files were pushed to DVC remote storage (Google Drive) using `dvc push`.
   
4. **Versioning Meta-data:**
   - DVC automatically tracked metadata changes, associating them with respective data files, ensuring a history of changes.

### pythan script
- A Python script (`DataExtraction_and_DataTransformation.py`) carries out data extraction, transformation, and storage.
- Ensured all necessary dependencies are installed (`requirements.txt`, `Pipfile.lock`).
- Check processed data files (`dawn_processed_data.txt` and `bbc_processed_data.txt`) for output.

### DAG script:
- DAG script is written in python to automate Data extraction , transformationa and versioning.

## Contribution:
- Contributions and feedback are welcome. Please open an issue or submit a pull request.


## Contact:
- For further assistance or inquiries, contact [ Sehrish khan ](sehrishkhanhumayun@gmail.com).
