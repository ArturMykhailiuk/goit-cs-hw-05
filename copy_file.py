import argparse
import asyncio
import logging
import os
import shutil

async def read_folder(source_folder, target_folder):
    async def _read_folder(path):
        tasks = []
        for entry in os.scandir(path):
            if entry.is_dir():
                tasks.append(_read_folder(entry.path))
            elif entry.is_file():
                tasks.append(copy_file(entry.path, source_folder, target_folder))
        await asyncio.gather(*tasks)

    await _read_folder(source_folder)

async def copy_file(file_path, source_folder, target_folder):
    try:
        extension = os.path.splitext(file_path)[1]
        target_path = os.path.join(target_folder, extension[1:])
        os.makedirs(target_path, exist_ok=True)
        shutil.copy(file_path, target_path)
    except Exception as e:
        logging.error(f"Failed to copy file: {file_path}\n{str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder', help='Source folder path')
    parser.add_argument('target_folder', help='Target folder path')
    args = parser.parse_args()

    source_folder = args.source_folder
    target_folder = args.target_folder

    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    asyncio.run(read_folder(source_folder, target_folder))