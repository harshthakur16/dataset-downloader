#Dataset Downloader


##Prerequisites

Download Python

During installation, make sure to check the box that says "Add Python to PATH".

⚙️ Setup Instructions
Follow these simple steps to get the tool ready.

1. Download the Project
Download this project folder to your computer. You can do this by clicking the "Code" button on the repository page and selecting "Download ZIP".

2. Unzip the Folder
Find the downloaded .zip file and unzip it. This will create a folder named dataset-downloader-main (or similar). You can rename it to dataset-downloader.

3. Set Your API Key
Your secret API key is needed to access the data.

Inside the project folder, find the file named .env.example.

Make a copy of this file and rename the copy to .env.

Open the new .env file with a simple text editor (like Notepad or TextEdit).

You will see this line: API_KEY=YOUR_API_KEY_HERE

Replace YOUR_API_KEY_HERE with your actual API key and save the file.

4. Install Dependencies
This step installs the necessary Python libraries for the script to work.

Open a terminal or command prompt inside the dataset-downloader folder.

Windows: Go into the folder, hold down the Shift key, right-click on an empty space, and select "Open PowerShell window here" or "Open in Terminal".

Mac: Open the "Terminal" app, type cd , drag the dataset-downloader folder from Finder into the Terminal window, and press Enter.

In the terminal, type the following command and press Enter:

pip install -r requirements.txt

▶️ How to Run the Script
Once the setup is complete, you can run the script anytime you need to download the data.

Make sure your terminal is still open in the dataset-downloader folder.

Run the script with this command:

python main.py

You will see status messages like "Downloading data..." and "Processing complete!".

✅ Output
After the script finishes, a new file named dataset.csv will be created in the same folder. This file contains your refined data, including the new columns derived from ad_creative.