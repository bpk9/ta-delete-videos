# MIT License
# 
# Copyright (c) 2025 Dhs92
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import argparse
import time

def delete_video(api_key: str, video_id: str, url: str) -> str:
    """
    Deletes a YouTube video using the tubearchivist API.
    Args:
        api_key (str): Your tubearchivist API key.
        video_id (str): The ID of the video to delete.
        tubearchivist_url (str): The base URL of your tubearchivist instance (without trailing slash).
    Returns:
        response (str): Response from the API.
    """
    url = f"{url}/api/video/{video_id}"
    headers = {
        'Authorization': f'Token {api_key}'
    }
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return f"Video with ID {video_id} deleted successfully."
    elif response.status_code == 404:
        return f"Video with ID {video_id} not found."
    else:
        return f"Failed to delete video with ID {video_id}. Status code: {response.status_code}, Response: {response.text}"
    
def get_videos(api_key: str, url: str) -> list:
    """
    Retrieves a list of all downloaded videos from the tubearchivist API.
    Args:
        api_key (str): Your tubearchivist API key.
        tubearchivist_url (str): The base URL of your tubearchivist instance (without trailing slash).
    Returns:
        list (list): A list of videos (dict) retrieved from the API.
    
    """

    # TubeArchivist API endpoint for retrieving all videos
    url = f"{url}/api/video/"

    videos = []
    page = 1
    headers = {
        'Authorization': f'Token {api_key}'
    }
    
    while True:
        response = requests.get(f'{url}?page={page}', headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve videos. Status code: {response.status_code}, Response: {response.text}, Page: {page}")
            break
        
        data = response.json()
        videos.extend(data['data'])
        
        # Check if we've reached the last page
        if page >= data['paginate']['last_page']:
            break
        page += 1
    
    return videos
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete all downloaded YouTube videos using the tubearchivist API.")
    parser.add_argument('--api-key', type=str, help="Your tubearchivist API key.", required=True)
    parser.add_argument('--url', type=str, help="Your tubearchivist URL without the trailing slash (https://yt.example.com).", required=True)
    parser.add_argument('--dry-run', action='store_true', help="Run the script in dry run mode (no videos will be deleted).", default=False)
    args = parser.parse_args()

    if args.dry_run:
        print("Running in dry run mode. No videos will be deleted.")
    else:
        print("!!! Running in normal mode. Videos will be deleted. !!!")
        print("!!! Press Ctrl+C to cancel. !!!")
        for i in range(5):
            time.sleep(1)
    
    videos = get_videos(args.api_key, args.url)

    if not videos:
        print("No videos found.")
    for video in videos:
        video_id = video.get('youtube_id')
        if video_id and not args.dry_run:
            print(f"Deleting video with ID: {video_id}")
            result = delete_video(args.api_key, video_id, args.url)
            print(result)
        elif args.dry_run:
            print(f"[DRY RUN] Would delete video with ID: {video_id}")
        else:
            print("No video ID found for the video.")
