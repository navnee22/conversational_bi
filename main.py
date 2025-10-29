from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator.mcp_client import get_table_metadata
from orchestrator.bedrock_client import generate_sql_from_prompt
from orchestrator.query_executor import run_query
from orchestrator.tableau_client import create_tableau_dashboard

app = FastAPI(title="Conversational BI Orchestrator")

class QueryRequest(BaseModel):
    user_query: str
    data_source: str
    create_dashboard: bool = False

@app.post("/query")
async def process_query(req: QueryRequest):
    try:
        # Step 1: Fetch metadata from Tableau MCP
        metadata = get_table_metadata(req.data_source)

        # Step 2: Send prompt + schema to Bedrock
        sql_query = generate_sql_from_prompt(req.user_query, metadata)

        # Step 3: Execute query in DW
        results = run_query(sql_query)

        # Step 4 (Optional): Create Tableau dashboard
        if req.create_dashboard:
            dashboard_url = create_tableau_dashboard(results)
            return {"sql": sql_query, "dashboard": dashboard_url}

        return {"sql": sql_query, "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
