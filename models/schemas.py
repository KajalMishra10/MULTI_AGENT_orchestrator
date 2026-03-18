from pydantic import BaseModel, Field


# Reviewer Output
class ReviewResult(BaseModel):
    approved: bool
    score: int
    feedback: str = ""


# PM Agent Output
class SRS(BaseModel):
    product_overview: str
    target_users: list[str]
    features: list[str]


# Test Manager Output
class TestStrategy(BaseModel):
    scope: str
    test_types: list[str]
    environment: str
    risks: list[str]


# Test Lead Output
class ExecutionPlan(BaseModel):
    test_phases: list[str]
    timeline: str
    resources: list[str]


# Manual QA Output
class ManualTestCase(BaseModel):
    test_id: str = ""
    title: str = ""
    steps: list[str] = []
    expected_result: str = ""


class ManualTests(BaseModel):
    manual_tests: list[ManualTestCase] = Field(default_factory=list)


# Automation QA Output
class AutomationScript(BaseModel):
    script_id: str = ""
    title: str = ""
    code: str = ""


class AutomationTests(BaseModel):
    automation_scripts: list[AutomationScript] = Field(default_factory=list)
