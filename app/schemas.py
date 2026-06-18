from pydantic import BaseModel, Field, ConfigDict


class GameplayMetrics(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "gameplay_duration_seconds": 120,
                "fruits_sliced": 85,
                "fruits_missed": 10,
                "bombs_hit": 1,
                "bombs_dodged": 8,
                "max_combo": 12,
                "pause_count": 1,
                "retries": 0,
                "overall_score": 950,
            }
        }
    )

    session_duration_seconds: int = Field(
        ...,
        alias="gameplay_duration_seconds",
        description="Total gameplay session duration in seconds",
        ge=0,
    )
    fruits_sliced: int = Field(..., description="Number of valid fruits successfully sliced", ge=0)
    fruits_missed: int = Field(..., description="Number of fruits missed", ge=0)
    bombs_hit: int = Field(..., description="Number of bombs accidentally hit", ge=0)
    bombs_dodged: int = Field(..., description="Number of bombs successfully dodged", ge=0)
    max_combo: int = Field(..., description="Maximum consecutive fruit slicing streak", ge=0)
    pause_count: int = Field(..., description="Number of times the game was paused", ge=0)
    retries: int = Field(..., description="Number of times the session was restarted", ge=0)
    overall_score: int = Field(..., description="Raw score from the game engine", ge=0)


class DerivedRatesResponse(BaseModel):
    accuracy_rate: float = Field(..., description="Calculated Accuracy Rate (0-100)")
    response_rate: float = Field(..., description="Calculated Response Rate (0-100)")
    error_rate: float = Field(..., description="Calculated Error Rate (0-100)")
    persistence_rate: float = Field(..., description="Calculated Persistence Rate (0-100)")
    consistency_rate: float = Field(..., description="Calculated Consistency Rate (0-100)")
    overall_performance_score: float = Field(
        ..., description="Calculated Overall Performance Score (0-100)"
    )
