import subprocess
import os


def wav_converter(name_of_vedio:str):
# Define the ffmpeg command
    output_file =name_of_vedio.replace(".mp3",".wav") 
    command = fr'ffmpeg -i "{os.path.realpath("vedio_data")+"\\"+name_of_vedio}" -ac 1 -ar 16000 "{os.path.realpath("vedio_data")+"\\"+output_file}"'
    
    
    try:
#         # Run the command
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            encoding="utf-8"  # Ensures proper encoding
        )        
        # Print success message and output
        print("Conversion completed successfully.")
        print("Output:")
        print(result.stdout)
        return output_file
    except subprocess.CalledProcessError as e:
        # Handle errors
        print(f"Command failed with return code {e.returncode}")
        print(f"Error output: {e.stderr}")
    finally:
        mp3_file_deletion(f"{os.path.realpath("vedio_data")}\{name_of_vedio}")
def mp3_file_deletion(mp3_file):
    try:
        if os.path.exists(mp3_file):
            os.remove(mp3_file)
            os.close()
            print(f"file has been deleted successfully.")
        else:
            print(f"The file does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")

