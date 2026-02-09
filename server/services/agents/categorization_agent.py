from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import List
from dataclasses import dataclass

from models.schemas import Bucket, EmailThread

# Set up Jinja2 environment
# Path to prompts folder: server/services/prompts
template_dir = Path(__file__).parent.parent / "prompts"
jinja_env = Environment(loader=FileSystemLoader(template_dir))

class EmailCategoryOutput(BaseModel):
    thread_id: str
    bucket_id: str

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
# TODO: Output Typing
def instructions(ctx:RunContext[CategorizationAgentDeps]) -> List[dict]:
    
    deps = ctx.deps
    emails = deps.emails
    buckets = deps.buckets
    
    template = jinja_env.get_template("categorization_template.jinja2")

    return template.render(emails=emails, buckets=buckets)


    
