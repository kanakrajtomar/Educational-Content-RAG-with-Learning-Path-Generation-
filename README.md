##Educational Content RAG

## Install Dependencies

Before installing the dependencies listed in `requirements.txt`, follow these steps to avoid issues with `onnxruntime` installation:

1. **Install Microsoft C++ Build Tools**

   * Follow this guide: [Install VS Build Tools for Windows](https://github.com/bycloudai/InstallVSBuildToolsWindows?tab=readme-ov-file).
   * Complete all steps, including setting the environment variable path.

2. **Install project dependencies**

```bash
pip install -r requirements.txt
```

3. **Install markdown dependencies**

```bash
pip install "unstructured[md]"
```

---

## Create the Database

Run the following command to create the Chroma DB:

```bash
python create_database.py
```

---

## Query the Database

To query the Chroma DB, use:

```bash
python query_data.py "Your question here"
```

**Note:** For testing you can use your openai api key !
