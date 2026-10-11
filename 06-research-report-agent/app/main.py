from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI(title="Source-Traceable Research Report Demo")

class SourceNote(BaseModel):
    source_id: str = Field(min_length=1, max_length=40)
    title: str = Field(min_length=1, max_length=200)
    url: HttpUrl
    notes: str = Field(min_length=5, max_length=5000)

class ReportIn(BaseModel):
    research_question: str = Field(min_length=5, max_length=1000)
    sources: list[SourceNote] = Field(min_length=1, max_length=20)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reports/draft")
def draft_report(payload: ReportIn):
    source_sections = []
    for source in payload.sources:
        source_sections.append({
            "source_id": source.source_id,
            "title": source.title,
            "url": str(source.url),
            "notes": source.notes,
            "claims_supported": ["Only the supplied notes; reviewer must verify."]
        })
    draft = [
        f"# Research draft: {payload.research_question}",
        "",
        "## Executive summary",
        "Draft summary pending human synthesis and verification of the supplied source notes.",
        "",
        "## Evidence collected",
    ]
    for source in payload.sources:
        draft += [f"### [{source.source_id}] {source.title}",
                  f"Source: {source.url}", source.notes, ""]
    draft += [
        "## Analysis",
        "Compare sources against explicit criteria. Do not infer facts that are not present in the notes.",
        "",
        "## Gaps and limitations",
        "- The system did not independently open or verify the URLs.",
        "- Notes may be incomplete or outdated.",
        "- All claims and citations require human review before publication.",
    ]
    return {
        "research_question": payload.research_question,
        "draft_markdown": "\n".join(draft),
        "sources": source_sections,
        "status": "draft_requires_human_verification"
    }
