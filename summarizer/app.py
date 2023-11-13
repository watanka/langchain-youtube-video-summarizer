from langchain.prompts import PromptTemplate
from langchain.schema import runnable, Document
from typing import Dict, List

from fastapi import FastAPI
from langserve import add_routes
import uvicorn
from summary_chain import map_reduce

app = FastAPI()


@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}




add_routes(
    app,
    map_reduce,
    path = '/summarize',
    input_type = List[Document],
    config_keys = {'concurrency'}
)

# add_routes(
#     app,
#     rag_chain,
#     path = '/llama-cpp-rag'
# )

# document_prompt = PromptTemplate.from_template('{page_content}')
# map_prompt = '''
# summarize this content: 
# {context}
# '''

# if __name__ == '__main__' :
#     uvicorn.run(app, host = '127.0.0.1', port = 6500)