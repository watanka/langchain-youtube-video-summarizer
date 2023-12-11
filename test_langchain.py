from summarizer import summary_chain, text_split
from typing import List
from langchain.schema import Document
from pydantic import BaseModel

class SummaryResult(BaseModel) :
    summary : str

random_text = "Each of these commands is capable of fulfilling the task at hand. However, it's important to note that the debugfs command offers additional information, including access time (atime), change time (ctime), and modification time (mtime), alongside creation time (crtime). However, debugfs requires you to find out both the file path and the filesystem device. This requirement means you'll need to execute two additional commands before you can even run the debugfs command."

docs = text_split.split_docs(random_text)

mapreduce_function = summary_chain.map_reduce

mapreduce_function.with_config(input_type = List[Document], output = SummaryResult)

result = mapreduce_function.invoke(docs)

print(result)