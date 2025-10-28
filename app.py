import asyncio
import aiohttp
import requests
import time
import streamlit as st
from urllib.parse import urlparse
import os
import concurrent.futures

class GitHubRepoFetcher:
    def __init__(self, base_url):
        self.base_url = base_url
        self.repo_name, self.user_name = self.fetch_repo_details()
        self.api_url = f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/contents"

    def fetch_repo_details(self):
        path_parts = urlparse(self.base_url).path.strip("/").split("/")
        if len(path_parts) >= 2:
            return path_parts[1], path_parts[0]
        else:
            raise ValueError("Invalid GitHub URL")


class SyncFetcher:
    def __init__(self, api_url):
        self.api_url = api_url

    def traverse(self, api_url):
        file_contents = []
        response = requests.get(api_url)
        response.raise_for_status()
        items = response.json()

        for item in items:
            if item['type'] == 'file':
                res = requests.get(item['download_url'])
                res.raise_for_status()
                file_contents.append({'path': item['path'], 'content': res.text})
            elif item['type'] == 'dir':
                file_contents.extend(self.traverse(item['url']))
        return file_contents

    def run(self):
        start = time.time()
        files = self.traverse(self.api_url)
        elapsed = time.time() - start
        return len(files), elapsed


class AsyncFetcher:
    def __init__(self, api_url):
        self.api_url = api_url

    async def download_and_append(self, item, session, path):
        async with session.get(item["download_url"]) as res:
            res.raise_for_status()
            content_type = res.headers.get("Content-Type", "")

            if "text" not in content_type and "json" not in content_type:
                # print(f"Skipping binary file: {item['path']} ({content_type})")
                return

            content = await res.text()
            # print(f"Saved: {item['path']}")

            header = f"\n\n==== {item['path']} ====\n"
            async with asyncio.Lock():
                with open(path, "a", encoding="utf-8") as cf:
                    cf.write(header)
                    cf.write(content)
            
            return item['path']

    async def traverse(self, api_url, session, path="combined.txt"):
        async with session.get(api_url) as response:
            response.raise_for_status()
            items = await response.json()

        tasks = []
        files = []
        
        for item in items:
            if item["type"] == "file":
                tasks.append(self.download_and_append(item, session, path))
            elif item["type"] == "dir":
                sub_files = await self.traverse(item["url"], session, path)
                if sub_files:
                    files.extend(sub_files)
        if tasks:
            results = await asyncio.gather(*tasks)
            files.extend([r for r in results if r])
        
        return files

    async def run(self):
        start = time.time()
        async with aiohttp.ClientSession() as session:
            files = await self.traverse(self.api_url, session)
        elapsed = time.time() - start
        return len(files), elapsed


# ---------------------- STREAMLIT APP ---------------------- #
st.title("⚡ Async vs Sync GitHub Repo Fetcher")

base_url = st.text_input("Enter GitHub Repository URL:", placeholder="https://github.com/AdityaZala3919/sample-repository")

if st.button("Run Comparison"):
    repo_fetcher = GitHubRepoFetcher(base_url)

    sync_fetcher = SyncFetcher(repo_fetcher.api_url)
    async_fetcher = AsyncFetcher(repo_fetcher.api_url)

    # Synchronous fetch with progress bar
    sync_progress = st.progress(0)
    sync_status = st.empty()
    sync_status.text("Running synchronous (requests) fetch...")
    with concurrent.futures.ThreadPoolExecutor() as ex:
        future = ex.submit(sync_fetcher.run)
        pct = 0
        while not future.done():
            pct = min(99, pct + 3)
            sync_progress.progress(pct)
            time.sleep(0.25)
        sync_count, sync_time = future.result()
        sync_progress.progress(100)
    sync_status.text(f"Synchronous fetch completed in {sync_time:.2f}s")

    # Asynchronous fetch with progress bar
    async_progress = st.progress(0)
    async_status = st.empty()
    async_status.text("Running asynchronous (aiohttp) fetch...")
    with concurrent.futures.ThreadPoolExecutor() as ex:
        future = ex.submit(lambda: asyncio.run(async_fetcher.run()))
        pct = 0
        while not future.done():
            pct = min(99, pct + 3)
            async_progress.progress(pct)
            time.sleep(0.05)
        async_count, async_time = future.result()
        async_progress.progress(100)
    async_status.text(f"Asynchronous fetch completed in {async_time:.2f}s")

    st.success("✅ Fetching Completed!")

    st.subheader("📊 Results")
    st.write(f"**Repository:** {repo_fetcher.user_name}/{repo_fetcher.repo_name}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sync Files Fetched", sync_count)
        st.metric("Sync Time (s)", f"{sync_time:.2f}")
    with col2:
        st.metric("Async Files Fetched", async_count)
        st.metric("Async Time (s)", f"{async_time:.2f}")
    
    download_path = "combined.txt"
    if os.path.exists(download_path) and os.path.getsize(download_path) > 0:
        with open(download_path, "rb") as f:
            data = f.read()
        filename = f"{repo_fetcher.user_name}-{repo_fetcher.repo_name}-combined.txt"
        st.download_button("Download extracted .txt", data, file_name=filename, mime="text/plain")
    else:
        st.info("No extracted .txt available for download (combined.txt not found or empty).")
