from config import FILE_MAXSIZE

description = f"""
Temporary storage for files.

Put file -> Recieve ID.  
Put ID   -> Recieve file.  
Easy.

Current config:  
**Max file size: {FILE_MAXSIZE} Mb**
"""

tags = [
    {
        "name": "File Service",
        "description": "The main logic routes."
    }
]
