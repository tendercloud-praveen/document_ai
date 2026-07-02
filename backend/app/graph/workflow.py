from langgraph.graph import StateGraph, START, END

from app.graph.state import DocumentState
from app.graph.nodes import upload_node, ocr_node, llm_node


workflow = StateGraph(DocumentState)
workflow.add_node("upload", upload_node)
workflow.add_node("ocr", ocr_node)
workflow.add_node("llm", llm_node)
workflow.add_edge(START, "upload")
workflow.add_edge("upload", "ocr")
workflow.add_edge("ocr", "llm")
workflow.add_edge("llm", END)
graph = workflow.compile()