import requests
from bs4 import BeautifulSoup
import re
import os
import json

def download_pinterest_media(url, output_folder="downloads"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Не удалось получить страницу.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    video_url = None
    image_urls = []

    # Поиск видео через meta
    meta_video = soup.find("meta", property="og:video")
    if meta_video and meta_video.get("content"):
        video_url = meta_video["content"]

    # Поиск видео через ld+json
    if not video_url:
        for script in soup.find_all("script", {"type": "application/ld+json"}):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and "contentUrl" in data:
                    video_url = data["contentUrl"]
            except Exception:
                continue

    # Поиск через raw-скрипты
    if not video_url:
        scripts = soup.find_all("script")
        for script in scripts:
            if not script.string:
                continue
            match = re.search(r'"contentUrl":"(https://v\.pinimg\.com/videos/[^"]+)"', script.string)
            if match:
                video_url = match.group(1)
                break

    # Если найдено видео — скачиваем только его
    if video_url:
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, "pinterest_video.mp4")
        try:
            video_resp = requests.get(video_url, headers=headers)
            if video_resp.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(video_resp.content)
                return file_path
            else:
                print("Ошибка при скачивании видео.")
        except Exception as e:
            print(f"Ошибка: {e}")
        return

    # Если видео нет — ищем картинки
    meta_image = soup.find("meta", property="og:image")
    if meta_image and meta_image.get("content"):
        image_urls.append(meta_image["content"])

    for script in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and "image" in data:
                if isinstance(data["image"], list):
                    for img in data["image"]:
                        image_urls.append(img)
                elif isinstance(data["image"], str):
                    image_urls.append(data["image"])
        except Exception:
            continue

    scripts = soup.find_all("script")
    for script in scripts:
        if not script.string:
            continue
        image_matches = re.findall(r'"url":"(https://i\.pinimg\.com/originals/[^"]+)"', script.string)
        image_urls.extend(image_matches)

    # Сохраняем только уникальные картинки
    image_urls = list(dict.fromkeys(image_urls))

    if not image_urls:
        print("Фото не обнаружены.")
        return

    os.makedirs(output_folder, exist_ok=True)
    for i, img_url in enumerate(image_urls, start=1):
        file_path = os.path.join(output_folder, f"pinterest_image_{i}.jpg")
        try:
            img_resp = requests.get(img_url, headers=headers)
            if img_resp.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(img_resp.content)
                return file_path
            else:
                print(f"Ошибка при скачивании фото: {img_url}")
        except Exception as e:
            print(f"Ошибка: {e}")



