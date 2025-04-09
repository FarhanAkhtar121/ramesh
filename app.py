import asyncio
import time
import json
from typing import List, Dict
from praisonaiagents import Agent, Task, PraisonAIAgents
from duckduckgo_search import DDGS
from pydantic import BaseModel

class SearchResult(BaseModel):
    query: str
    results: List[Dict[str, str]]
    total_results: int

class ResearchDocument(BaseModel):
    title: str
    sections: List[Dict[str, str]]
    references: List[str]
    summary: str

async def async_search_tool(query: str) -> Dict:
    """Perform asynchronous search and return structured results."""
    await asyncio.sleep(1)  # Simulate network delay
    try:
        results = []
        ddgs = DDGS()
        for result in ddgs.text(keywords=query, max_results=5):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results)
        }
    except Exception as e:
        print(f"Error during async search: {e}")
        return {"query": query, "results": [], "total_results": 0}

async_agent = Agent(
    name="AsyncSearchAgent",
    role="Search Specialist",
    goal="Perform fast parallel searches with structured results",
    backstory="Expert in efficient data retrieval and parallel search operations",
    tools=[async_search_tool],
    self_reflect=False,
    verbose=True,
    markdown=True
)

summary_agent = Agent(
    name="SummaryAgent",
    role="Research Synthesizer",
    goal="Create concise summaries from multiple search results",
    backstory="Expert in analyzing and synthesizing information from multiple sources",
    self_reflect=True,
    verbose=True,
    markdown=True
)

async def run_parallel_tasks(): 
    """Run multiple async tasks in parallel"""
    print("\nRunning Parallel Async Tasks...")

    search_topics = [
        "Latest AI Developments 2024",
        "Upcoming AI technologies and trends in 2025",
        "AI Agents in 2025"
    ]
    
    parallel_tasks = [
        Task(
            name=f"search_task_{i}",
            description=f"Search for '{topic}' and return structured results.",
            expected_output="SearchResult model with search data",
            agent=async_agent,
            async_execution=True,
            output_json=SearchResult
        ) for i, topic in enumerate(search_topics)
    ]
    
    summary_task = Task(
        name="summary_task",
        description="Analyze all search results and create a concise summary.",
        expected_output="Well-structured research document in Markdown format",
        agent=summary_agent,
        async_execution=False,
        context=parallel_tasks
    )
    
    agents = PraisonAIAgents(
        agents=[async_agent, summary_agent],
        tasks=parallel_tasks + [summary_task],
        verbose=1,
        process="sequential"
    )
    
    results = await agents.astart()

    # Save research results
    with open('/tmp/research.md', 'w') as f:
        f.write(json.dumps(results, indent=4))
    
    return results

async def main():
    start_time = time.time()
    results = await run_parallel_tasks()
    end_time = time.time()
    
    print(f"\nResearch completed in {end_time - start_time:.2f} seconds")
    print(f"Results saved to /tmp/research.md")
    
    # Print a summary of the results
    if results and isinstance(results, dict):
        for task_name, task_result in results.items():
            if task_name.startswith("search_task_"):
                search_data = task_result.get("result", {})
                if search_data:
                    print(f"\nSearch for '{search_data.get('query', 'Unknown')}' found {search_data.get('total_results', 0)} results")
            elif task_name == "summary_task":
                print("\nSummary task completed successfully")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())