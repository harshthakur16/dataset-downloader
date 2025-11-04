import os
import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

def fetch_data(url):
    """Fetches data from the given URL and returns the content."""
    print("Downloading data...")
    try:
        response = requests.get(url, timeout=30)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        print("Download successful.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def process_csv_data(csv_content):
    """
    Processes the raw CSV string into a refined pandas DataFrame.
    It splits the 'ad_creative' column into multiple new columns.
    """
    if not csv_content:
        return None

    print("Processing data...")
    try:
        # Use StringIO to treat the string data as a file
        data_file = StringIO(csv_content)
        df = pd.read_csv(data_file)

        # Preserve the original ad_creative column by making a copy to split
        ad_creative_series = df['ad_creative'].str.strip()

        # Split the 'ad_creative' column into new columns.
        # n=5 ensures that we split at most 5 times, leaving the rest in the last column.
        # This handles cases where 'otherData' might contain underscores.
        split_columns = ad_creative_series.str.split('_', n=4, expand=True)

        # Create new columns with camelCase names
        new_column_names = {
            0: 'category',
            1: 'scriptName',
            2: 'actorName',
            3: 'formatName',
            4: 'otherData'
        }
        df_new_columns = split_columns.rename(columns=new_column_names)

        # Combine the original dataframe with the new columns
        # Place the new columns right after the original 'ad_creative' column
        ad_creative_index = df.columns.get_loc('ad_creative')
        
        # Combine all parts into the final dataframe
        df_final = pd.concat([
            df.iloc[:, :ad_creative_index + 1], 
            df_new_columns, 
            df.iloc[:, ad_creative_index + 1:]
        ], axis=1)

        print("Processing complete.")
        return df_final

    except KeyError:
        print("Error: 'ad_creative' column not found in the dataset.")
        return None
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        return None

def save_data_to_csv(data_frame, file_path):
    """Saves the DataFrame to a CSV file."""
    if data_frame is not None:
        try:
            # Get the directory part of the file path
            directory = os.path.dirname(file_path)
            # Create the directory if it doesn't exist
            if directory:
                os.makedirs(directory, exist_ok=True)
                
            data_frame.to_csv(file_path, index=False)
            print(f"Data successfully saved to {file_path}")
        except Exception as e:
            print(f"Could not save the file. Error: {e}")

def main():
    """Main function to orchestrate the download, processing, and saving."""
    # Load environment variables from a .env file
    load_dotenv()

    api_key = os.getenv("API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("Error: API_KEY not found or not set.")
        print("Please create a .env file and set your API_KEY.")
        return

    base_url = "https://analytics.seekho.in/api/queries/46930/results.csv"
    full_url = f"{base_url}?api_key={api_key}"
    
    # --- CHANGE: Define output directory and create full path ---
    output_dir = "output"
    output_filename = "dataset.csv"
    # os.path.join creates a correct path like "output/dataset.csv"
    output_filepath = os.path.join(output_dir, output_filename)

    csv_data = fetch_data(full_url)
    if csv_data:
        processed_data_frame = process_csv_data(csv_data)
        # --- CHANGE: Pass the new full file path to the save function ---
        save_data_to_csv(processed_data_frame, output_filepath)

if __name__ == "__main__":
    main()

