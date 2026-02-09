from dataclasses import dataclass
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader
from models.schemas import Bucket, EmailThread
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

# Set up Jinja2 environment
# Path to prompts folder: server/services/prompts
template_dir = Path(__file__).parent.parent / "prompts"
jinja_env = Environment(loader=FileSystemLoader(template_dir))

class EmailCategoryOutput(BaseModel):
    thread_id: str
    bucket_id: str
    bucket_name: str

@dataclass
class CategorizationAgentDeps:
    buckets: List[Bucket]
    emails: List[EmailThread]
    
    
categorization_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest",
    output_type = List[EmailCategoryOutput],
    output_retries=3
)

@categorization_agent.instructions
def instructions(ctx: RunContext[CategorizationAgentDeps]) -> str:
    
    deps = ctx.deps
    emails = deps.emails
    buckets = deps.buckets
    
    template = jinja_env.get_template("categorization_template.jinja2")

    return template.render(emails=emails, buckets=buckets)


    
