from pydantic import BaseModel, Field


class Room(BaseModel):
    name: str = Field(
        ...,
        description="Name or label of the room/space (e.g., 'Master Bedroom', 'Kitchen', 'Living Room', 'Bathroom')."
    )
    area: float | None = Field(
        default=None,
        gt=0,
        description="Total floor area of the room in square meters (m²)."
    )
    width: float | None = Field(
        default=None,
        gt=0,
        description="Width of the room in meters."
    )
    length: float | None = Field(
        default=None,
        gt=0,
        description="Length of the room in meters."
    )


class Wall(BaseModel):
    length: float | None = Field(
        default=None,
        gt=0,
        description="Total length of the wall segment in meters."
    )
    thickness: float | None = Field(
        default=None,
        gt=0,
        lt=1.5,
        description="Thickness of the wall in meters (typically between 0.10m and 0.50m)."
    )
    height: float | None = Field(
        default=None,
        gt=0,
        description="Wall height in meters (floor-to-ceiling height)."
    )


class Opening(BaseModel):
    width: float | None = Field(
        default=None,
        gt=0,
        description="Width of the door or window opening in meters."
    )
    height: float | None = Field(
        default=None,
        gt=0,
        description="Height of the door or window opening in meters."
    )
    quantity: int = Field(
        default=1,
        ge=1,
        description="Number of identical doors or windows with these dimensions."
    )


class Dimension(BaseModel):
    value: float = Field(
        ...,
        gt=0,
        description="Numeric value of the extracted quote or measurement dimension line."
    )
    unit: str = Field(
        default="m",
        description="Unit of measurement extracted from the floor plan (e.g., 'm', 'cm', 'mm')."
    )
    description: str | None = Field(
        default=None,
        description="Context or label associated with this dimension line (e.g., 'Total Facade Width', 'Hallway Length')."
    )


class PlanData(BaseModel):
    building_type: str | None = Field(
        default=None,
        description="Type or classification of the building (e.g., 'Residential', 'Commercial', 'Apartment', 'Single Family House')."
    )
    total_area: float | None = Field(
        default=None,
        gt=0,
        description="Total built area or footprint area of the architectural plan in square meters (m²)."
    )

    rooms: list[Room] = Field(
        default_factory=list,
        description="List of all distinct rooms and spaces identified in the floor plan."
    )
    walls: list[Wall] = Field(
        default_factory=list,
        description="List of major wall segments or structural wall specifications identified."
    )
    doors: list[Opening] = Field(
        default_factory=list,
        description="List of all doors identified in the floor plan with their dimensions and counts."
    )
    windows: list[Opening] = Field(
        default_factory=list,
        description="List of all windows identified in the floor plan with their dimensions and counts."
    )
    dimensions: list[Dimension] = Field(
        default_factory=list,
        description="List of general dimension lines, cotas, or annotations explicitly written on the plan."
    )

SYSTEM_PROMPT = "You are an expert architectural AI assistant specialized in analyzing and "
"extracting structured data from floor plans and blueprints.\n\n"
"Guidelines:\n"
"- Carefully examine the provided image for room names, doors, windows, dimensions, and wall indicators.\n"
"- Convert all extracted physical measurements to meters (m) and area measurements to square meters (m²).\n"
"- If a dimension is explicitly labeled, record it under 'dimensions'.\n"
"- Be precise and leave optional fields as null if they cannot be determined from the image."
