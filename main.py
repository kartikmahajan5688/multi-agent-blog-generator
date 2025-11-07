"""
Multi-Agent Blog Generator using LangChain (RunnableSequence)
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.runnables import RunnableSequence, RunnableLambda

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"🔑 OpenAI API Key Loaded: {'Yes' if OPENAI_API_KEY else 'No'}")

app = FastAPI(title="Multi-Agent Blog Generator (LangChain RunnableSequence)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------


class BlogRequest(BaseModel):
    topic: str
    tone: str = "professional"
    length: str = "medium"  # short, medium, long


class BlogResponse(BaseModel):
    topic: str
    research: str
    draft: str
    final_blog: str
    status: str

# -----------------------------------------------------------------------------
# LLM
# -----------------------------------------------------------------------------


def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=api_key)


llm = get_llm()

# -----------------------------------------------------------------------------
# Agents as functions
# -----------------------------------------------------------------------------


def research_agent(inputs):
    topic = inputs["topic"]
    tone = inputs["tone"]
    length = inputs["length"]

    prompt = f"""
You are a research agent. Research the topic: "{topic}"

Provide:
1. Key points to cover
2. Important facts and statistics
3. Structured outline for a {length} blog post
4. Relevant angles and perspectives

Tone: {tone}
    """

    result = llm.invoke([HumanMessage(content=prompt)])
    return {**inputs, "research": result.content}


def writer_agent(inputs):
    word_count = {
        "short": "500-700",
        "medium": "800-1200",
        "long": "1500-2000"
    }

    prompt = f"""
You are a professional blog writer. Write a complete blog post based on the following research:

Research:
{inputs['research']}

Requirements:
- Topic: {inputs['topic']}
- Tone: {inputs['tone']}
- Length: {word_count[inputs['length']]} words
- Engaging introduction, clear headings, strong conclusion, SEO-friendly.
    """

    result = llm.invoke([HumanMessage(content=prompt)])
    return {**inputs, "draft": result.content}


def reviewer_agent(inputs):
    prompt = f"""
You are an editorial reviewer. Review and polish this draft:

Draft:
{inputs['draft']}

Check for:
1. Grammar and spelling
2. Flow and readability
3. Tone consistency ({inputs['tone']})
4. SEO optimization

Return the final polished version.
    """

    result = llm.invoke([HumanMessage(content=prompt)])
    return {**inputs, "final_blog": result.content}


# -----------------------------------------------------------------------------
# Create LangChain RunnableSequence
# -----------------------------------------------------------------------------

blog_chain = RunnableLambda(research_agent) | RunnableLambda(
    writer_agent) | RunnableLambda(reviewer_agent)


# -----------------------------------------------------------------------------
# API Routes
# -----------------------------------------------------------------------------


@app.get("/")
def root():
    return {
        "message": "Multi-Agent Blog Generator API (LangChain Chaining)",
        "endpoints": {
            "/generate": "POST - Generate blog",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.0.0"}


@app.post("/generate", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    try:
        inputs = {
            "topic": request.topic,
            "tone": request.tone,
            "length": request.length
        }

        final_state = blog_chain.invoke(inputs)

        return BlogResponse(
            topic=request.topic,
            research=final_state.get("research", ""),
            draft=final_state.get("draft", ""),
            final_blog=final_state.get("final_blog", ""),
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------------------------------
# Run Server
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))


# Below is the complete code for ai-multi-agent-blog/main.py with LangGraph integration.

# """
# Multi-Agent AI Blog Generator
# Built with FastAPI + LangChain + LangGraph + OpenAI
# """

# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import TypedDict, Annotated, Sequence
# import operator
# from langgraph.graph import StateGraph, END
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# print(f"🔑 OpenAI API Key Loaded: {'Yes' if OPENAI_API_KEY else 'No'}")

# # Initialize FastAPI app
# app = FastAPI(title="Multi-Agent Blog Generator")

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Pydantic models for API


# class BlogRequest(BaseModel):
#     topic: str
#     tone: str = "professional"
#     length: str = "medium"  # short, medium, long


# class BlogResponse(BaseModel):
#     topic: str
#     research: str
#     draft: str
#     final_blog: str
#     status: str

# # State definition for LangGraph


# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], operator.add]
#     topic: str
#     tone: str
#     length: str
#     research: str
#     draft: str
#     final_blog: str
#     revision_count: int

# # Initialize OpenAI LLM (set your API key in environment)


# def get_llm():
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         raise ValueError("OPENAI_API_KEY not found in environment variables")
#     return ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=api_key)

# # Agent 1: Researcher


# def researcher_agent(state: AgentState) -> AgentState:
#     """Research agent gathers information and creates an outline"""
#     llm = get_llm()

#     prompt = f"""You are a research agent. Your task is to research the topic: "{state['topic']}"

#     Provide:
#     1. Key points to cover
#     2. Important facts and statistics (you can suggest what to research)
#     3. Structured outline for a {state['length']} blog post
#     4. Relevant angles and perspectives

#     Tone should be: {state['tone']}

#     Format your research clearly with sections."""

#     response = llm.invoke([HumanMessage(content=prompt)])

#     return {
#         **state,
#         "research": response.content,
#         "messages": [AIMessage(content=f"Research completed for: {state['topic']}")],
#     }

# # Agent 2: Writer


# def writer_agent(state: AgentState) -> AgentState:
#     """Writer agent creates the blog post based on research"""
#     llm = get_llm()

#     word_count = {
#         "short": "500-700",
#         "medium": "800-1200",
#         "long": "1500-2000"
#     }

#     prompt = f"""You are a professional blog writer. Using the research below, write a compelling blog post.

# Research:
# {state['research']}

# Requirements:
# - Topic: {state['topic']}
# - Tone: {state['tone']}
# - Length: {word_count[state['length']]} words
# - Include an engaging introduction
# - Use clear headings and subheadings
# - Add a strong conclusion with call-to-action
# - Make it SEO-friendly

# Write the complete blog post now."""

#     response = llm.invoke([HumanMessage(content=prompt)])

#     return {
#         **state,
#         "draft": response.content,
#         "messages": state["messages"] + [AIMessage(content="Blog draft completed")],
#     }

# # Agent 3: Reviewer


# def reviewer_agent(state: AgentState) -> AgentState:
#     """Reviewer agent checks quality and makes final edits"""
#     llm = get_llm()

#     prompt = f"""You are an editorial reviewer. Review and polish this blog post.

# Draft:
# {state['draft']}

# Check for:
# 1. Grammar and spelling
# 2. Flow and readability
# 3. Tone consistency (should be {state['tone']})
# 4. Engagement factor
# 5. SEO optimization

# Provide the FINAL, POLISHED version of the blog post. Make it publication-ready."""

#     response = llm.invoke([HumanMessage(content=prompt)])

#     return {
#         **state,
#         "final_blog": response.content,
#         "revision_count": state.get("revision_count", 0) + 1,
#         "messages": state["messages"] + [AIMessage(content="Review and editing completed")],
#     }

# # Build the LangGraph workflow


# def create_workflow():
#     """Create the multi-agent workflow"""
#     workflow = StateGraph(AgentState)

#     # Add nodes (agents)
#     workflow.add_node("researcher", researcher_agent)
#     workflow.add_node("writer", writer_agent)
#     workflow.add_node("reviewer", reviewer_agent)

#     # Define the flow
#     workflow.set_entry_point("researcher")
#     workflow.add_edge("researcher", "writer")
#     workflow.add_edge("writer", "reviewer")
#     workflow.add_edge("reviewer", END)

#     return workflow.compile()


# # Create the workflow instance
# graph = create_workflow()

# # API Endpoints


# @app.get("/")
# def read_root():
#     return {
#         "message": "Multi-Agent Blog Generator API",
#         "endpoints": {
#             "/generate": "POST - Generate a blog post",
#             "/health": "GET - Check API health"
#         }
#     }


# @app.get("/health")
# def health_check():
#     return {"status": "healthy", "version": "1.0.0"}


# @app.post("/generate", response_model=BlogResponse)
# async def generate_blog(request: BlogRequest):
#     """Generate a blog post using the multi-agent system"""
#     try:
#         # Initialize state
#         initial_state = AgentState(
#             messages=[],
#             topic=request.topic,
#             tone=request.tone,
#             length=request.length,
#             research="",
#             draft="",
#             final_blog="",
#             revision_count=0
#         )

#         # Run the workflow
#         final_state = graph.invoke(initial_state)

#         return BlogResponse(
#             topic=request.topic,
#             research=final_state["research"],
#             draft=final_state["draft"],
#             final_blog=final_state["final_blog"],
#             status="success"
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.getenv("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)
