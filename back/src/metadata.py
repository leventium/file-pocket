from config import FILE_MAXSIZE, EXPIRE_TIME

description = f"""
Temporary storage for files.

Put file -> Recieve ID.  
Put ID   -> Recieve file.  
Easy.

**Current config:**  
**Max file size: {FILE_MAXSIZE} Mb**  
**Expire time: {EXPIRE_TIME} h**
"""

tags = [
    {
        "name": "File Service",
        "description": "The main logic routes."
    }
]
