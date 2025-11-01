# ⚡ Async vs Sync GitHub Repo Fetcher

Compare the performance of **synchronous** and **asynchronous** API calls when fetching files from a GitHub repository.
This project uses Python’s `requests` for sync fetching and `aiohttp` for async fetching, with a Streamlit interface to visualize performance differences.

---

## 🚀 Project Overview

This project demonstrates how **asynchronous programming** can outperform traditional synchronous API calls when dealing with multiple network requests.

Using the GitHub REST API, the app recursively fetches all files from a given repository and compares the runtime of:

* 🧩 **Synchronous fetch** using `requests`
* ⚡ **Asynchronous fetch** using `aiohttp` + `asyncio`

The app then displays:

* Time taken by each method
* Number of files fetched
* Download option for combined extracted file contents

---

## 🧠 Tech Stack

| Component   | Library / Tool                     | Description                                      |
| ----------- | ---------------------------------- | ------------------------------------------------ |
| Frontend    | **Streamlit**                      | Interactive UI for user input and visualization  |
| Sync Fetch  | **requests**                       | For blocking (synchronous) HTTP requests         |
| Async Fetch | **aiohttp**, **asyncio**           | For concurrent non-blocking requests             |
| Concurrency | **concurrent.futures**             | Runs sync and async fetchers in parallel threads |
| Utility     | **urllib.parse**, **os**, **time** | For URL parsing, file handling, and timing       |

---

## 📦 Project Structure

```
async-vs-sync-fetcher/
│
├── app.py                     # Main Streamlit app (this file)
├── LICENSE                    # MIT License
└── README.md                  # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AdityaZala3919/async-vs-sync-fetcher.git
   cd async-vs-sync-fetcher
   ```

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install streamlit requests aiohttp
   ```

4. **Run the Streamlit App**

   ```bash
   streamlit run app.py
   ```

---

## 💻 How It Works

### 1. User Input

Enter any **public GitHub repository URL** (e.g. `https://github.com/karpathy/nanoGPT`).

### 2. Sync Fetch

Uses Python’s `requests` library to fetch files **one by one**, blocking execution until each request completes.

### 3. Async Fetch

Uses `aiohttp` and `asyncio` to **fetch multiple files concurrently**, improving performance for I/O-bound operations.

### 4. Visualization

The app displays:

* Real-time progress bars for both methods
* Total execution time
* Number of files fetched
* Download option for the combined text file

---

## 📊 Example Output

| Mode                       | Files Fetched | Time (s) |
| -------------------------- | ------------- | -------- |
| **Synchronous (requests)** | 26            | 40.29    |
| **Asynchronous (aiohttp)** | 24            | 3.36     |

✅ **Result:** Async fetching is significantly faster for large repositories!

---

## 🧾 Notes

* Only **text-based files** (`.py`, `.txt`, `.md`, `.json`, etc.) are fetched; binary files are skipped.
* GitHub API rate limits may apply (60 requests/hour for unauthenticated users).
* The app writes fetched file contents to `combined.txt` for download.

---

## 🧑‍💻 Future Improvements

* Add GitHub authentication to increase rate limit.
* Visualize performance difference using charts.
* Support other APIs (e.g., Weather, OpenLibrary).
* Cache results to avoid redundant fetches.

---

## 🪪 License

This project is licensed under the **MIT License** — you’re free to use, modify, and distribute it.

---

## 🧑‍💻 Author

**Adityasinh Zala** <br>
AI/ML Engineer | Tech Explorer | Curious Learner   <br>
[GitHub](https://github.com/AdityaZala3919) • [LinkedIn](https://www.linkedin.com/in/adityasinh-zala-1bbb42258/)

---

⭐ *If you found this helpful, don’t forget to give it a star on GitHub!*
