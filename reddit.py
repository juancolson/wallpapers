import concurrent.futures
from dotenv import load_dotenv
from praw import Reddit
import os
from PIL import Image
import time

# Loading Environment Variables
load_dotenv(override=True)

# Loading Reddit Instance
reddit = Reddit(
    client_id=os.getenv("REDDIT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent="WallpaperBot/1.0.0",
    username=os.getenv("REDDIT_USERNAME"),
)

subReddit = reddit.subreddit('wallpapers_a')

source = os.path.join(os.getcwd(), "sources")

files = [f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))][:6]

def process_image(imagePath):
    try:
        image_path = os.path.join(source, imagePath)
        filename = os.path.splitext(os.path.basename(image_path))[0]
        meta = filename.split('@')[1].split('_with_')
        author = meta[0]
        name = meta[1]
        
        with Image.open(image_path) as img:
            width, height = img.size
        
        title = f'{name} by {author} ({width} x {height})'
        resp = subReddit.submit_image(title=title, image_path=image_path)
        return resp
    except Exception as e:
        return f"Error processing {imagePath}: {e}"


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        futures = {executor.submit(process_image, file): file for file in files}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)

start_time = time.time()
main()
end_time = time.time()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')