# API Contract — EcoBuild-AI

> **Version:** 1.0\
> **Status:** Draft / MVP\
> **API Style:** REST\
> **Base URL:** `/api/v1`

## 1. Overview

EcoBuild-AI is a platform that allows users to upload construction plans and generate analyses related to:

- required construction materials;
- estimated quantities;
- estimated project cost;
- potential material waste;
- estimated CO₂ savings;
- recommendations for reducing waste and unnecessary costs.

The application also provides a contextual chat associated with an analysis. Information provided by the user during the conversation may be used to generate a **new version of an existing analysis**.

The first version focuses on the core product flow:

```text
User
  ↓
Organization
  ↓
Plan Upload
  ↓
Plan Processing
  ↓
Analysis
  ↓
Materials + Cost + Sustainability Metrics
  ↓
Recommendations
  ↓
Chat
  ↓
New Analysis Version
```

---

# 2. Scope

## Included in the MVP

- User creation and persistence;
- Organization management;
- Construction plan upload;
- Plan processing status;
- Creation of multiple analyses for a plan;
- Analysis versioning;
- Material estimates;
- Estimated cost;
- Waste percentage;
- Estimated CO₂ savings;
- Recommendation generation;
- Analysis-related chat;
- Creation of new analysis versions from chat context.

## Out of Scope

The following features are intentionally excluded from the first version:

- JWT authentication;
- Login and logout;
- Refresh tokens;
- Persistent user sessions;
- Password recovery;
- Multi-user organizations;
- Roles and permissions;
- Supplier integration;
- Real-time material prices;
- Payment systems.

Authentication may be introduced in a future version without changing the core domain model.

---

# 3. Domain Entities

## 3.1 User

Represents the owner of one or more organizations.

```text
User
├── id
├── name
├── email
├── password_hash
├── created_at
└── updated_at
```

### Relationships

```text
User 1 ──────── * Organization
```

A user may own multiple organizations.

An organization belongs to only one user in the MVP.

---

## 3.2 Organization

Represents a company, construction business, or workspace where plans are managed.

```text
Organization
├── id
├── user_id
├── name
├── location
├── created_at
└── updated_at
```

### Relationships

```text
Organization
    │
    └──── * Plan
```

---

## 3.3 Plan

Represents an uploaded construction plan.

The uploaded file may initially be an image or PDF.

```text
Plan
├── id
├── organization_id
├── storage_ref
├── format
├── size
├── created_at
└── updated_at
```

### Plan Status

```text
uploaded
processing
ready
failed
```

### Processing Flow

```text
uploaded
    ↓
processing
    ↓
ready
```

If processing fails:

```text
processing
    ↓
failed
```

A plan may have multiple analyses.

```text
Plan 1 ──────── * Analysis
```

---

## 3.4 Analysis

Represents a material, cost, waste, and sustainability analysis generated from a construction plan.

```text
Analysis
├── id
├── plan_id
├── parent_analysis_id
├── version
├── estimated_cost
├── waste_percentage
├── co2_saved
├── status
├── created_at
└── updated_at
```

### Analysis Versioning

The first analysis has no parent:

```text
Analysis v1
parent_analysis_id = null
```

If the user provides additional context through the chat, a new analysis is created.

```text
Analysis v1
    │
    └── Analysis v2
            │
            └── Analysis v3
```

The original analysis is never overwritten.

### Example

```text
Analysis v1

Estimated Cost: 1,500,000 Kz
Cement: 100 bags
```

The user later provides additional information:

> The construction site is located in an area with higher transportation costs.

A new analysis is generated:

```text
Analysis v2

Estimated Cost: 1,750,000 Kz
Cement: 100 bags
```

---

## 3.5 Material Estimate

Represents an individual material estimated during an analysis.

```text
MaterialEstimate
├── id
├── analysis_id
├── material_name
├── quantity
├── unit
├── unit_price
├── total_cost
└── created_at
```

### Example

```json
{
    "material_name": "Cement",
    "quantity": 100,
    "unit": "bags",
    "unit_price": 7000,
    "total_cost": 700000
}
```

### Relationship

```text
Analysis 1 ──────── * MaterialEstimate
```

---

## 3.6 Recommendation

Represents a recommendation generated from an analysis.

Recommendations may focus on:

- reducing material waste;
- reducing unnecessary purchases;
- reducing costs;
- improving sustainability;
- suggesting more efficient purchasing strategies.

```text
Recommendation
├── id
├── analysis_id
├── title
├── description
├── impact
└── created_at
```

An analysis may have multiple recommendations.

```text
Analysis 1 ──────── * Recommendation
```

---

## 3.7 Chat

Represents a conversation related to an analysis.

```text
Chat
├── id
├── analysis_id
├── created_at
└── updated_at
```

---

## 3.8 Message

Represents a single message in a chat.

```text
Message
├── id
├── chat_id
├── role
├── content
└── created_at
```

### Message Roles

```text
user
assistant
```

### Relationship

```text
Chat 1 ──────── * Message
```

---

# 4. API Conventions

## Resource Naming

All routes use:

- lowercase;
- plural resource names;
- kebab-case when necessary.

Examples:

```text
/users
/organizations
/plans
/analyses
/recommendations
```

## HTTP Status Codes

| Status                      | Meaning                         |
| --------------------------- | ------------------------------- |
| `200 OK`                    | Successful request              |
| `201 Created`               | Resource successfully created   |
| `202 Accepted`              | Asynchronous processing started |
| `204 No Content`            | Resource successfully deleted   |
| `400 Bad Request`           | Invalid request                 |
| `404 Not Found`             | Resource not found              |
| `409 Conflict`              | Resource conflict               |
| `422 Unprocessable Entity`  | Validation error                |
| `500 Internal Server Error` | Unexpected server error         |

---

# 5. Users

## Create User

```http
POST /users
```

### Request

```json
{
    "name": "Emerson Albino",
    "email": "emerson@example.com",
    "password": "secure-password"
}
```

### Response — 201 Created

```json
{
    "id": "uuid",
    "name": "Emerson Albino",
    "email": "emerson@example.com",
    "created_at": "2026-08-19T10:00:00Z"
}
```

---

## Get User

```http
GET /users/{user_id}
```

### Response — 200 OK

```json
{
    "id": "uuid",
    "name": "Emerson Albino",
    "email": "emerson@example.com",
    "created_at": "2026-08-19T10:00:00Z"
}
```

---

# 6. Organizations

## Create Organization

```http
POST /users/{user_id}/organizations
```

### Request

```json
{
    "name": "Build Green Angola",
    "location": "Luanda, Angola"
}
```

### Response — 201 Created

```json
{
    "id": "uuid",
    "user_id": "uuid",
    "name": "Build Green Angola",
    "location": "Luanda, Angola",
    "created_at": "2026-08-19T10:00:00Z"
}
```

---

## List User Organizations

```http
GET /users/{user_id}/organizations
```

### Response — 200 OK

```json
[
    {
        "id": "uuid",
        "name": "Build Green Angola",
        "location": "Luanda, Angola"
    }
]
```

---

## Get Organization

```http
GET /organizations/{organization_id}
```

---

## Update Organization

```http
PATCH /organizations/{organization_id}
```

---

## Delete Organization

```http
DELETE /organizations/{organization_id}
```

### Response

```http
204 No Content
```

---

# 7. Plans

## Upload Plan

```http
POST /organizations/{organization_id}/plans
```

The request uses:

```text
multipart/form-data
```

### Fields

```text
file
```

The uploaded file may be:

```text
application/pdf
image/png
image/jpeg
```

### Response — 201 Created

```json
{
    "id": "uuid",
    "organization_id": "uuid",
    "file_name": "house-plan.pdf",
    "file_type": "application/pdf",
    "status": "uploaded",
    "created_at": "2026-08-19T10:00:00Z"
}
```

---

## List Organization Plans

```http
GET /organizations/{organization_id}/plans
```

---

## Get Plan

```http
GET /plans/{plan_id}
```

### Response

```json
{
    "id": "uuid",
    "organization_id": "uuid",
    "file_name": "house-plan.pdf",
    "status": "ready",
    "created_at": "2026-08-19T10:00:00Z"
}
```

---

## Process Plan

```http
POST /plans/{plan_id}/process
```

This operation starts the plan processing workflow.

### Response — 202 Accepted

```json
{
    "plan_id": "uuid",
    "status": "processing"
}
```

---

# 8. Analyses

## Create Analysis

```http
POST /plans/{plan_id}/analyses
```

The plan must have:

```text
status = ready
```

### Response — 202 Accepted

```json
{
    "id": "uuid",
    "plan_id": "uuid",
    "version": 1,
    "status": "processing"
}
```

The analysis is generated asynchronously.

---

## List Plan Analyses

```http
GET /plans/{plan_id}/analyses
```

### Response

```json
[
    {
        "id": "uuid",
        "version": 1,
        "estimated_cost": 1500000,
        "status": "ready",
        "created_at": "2026-08-19T10:00:00Z"
    },
    {
        "id": "uuid",
        "version": 2,
        "estimated_cost": 1750000,
        "status": "ready",
        "created_at": "2026-08-19T11:00:00Z"
    }
]
```

---

## Get Analysis

```http
GET /analyses/{analysis_id}
```

### Response

```json
{
    "id": "uuid",
    "plan_id": "uuid",
    "parent_analysis_id": null,
    "version": 1,
    "estimated_cost": 1500000,
    "waste_percentage": 4.5,
    "co2_saved": 120.5,
    "status": "ready",
    "materials": [
        {
            "id": "uuid",
            "material_name": "Cement",
            "quantity": 100,
            "unit": "bags",
            "unit_price": 7000,
            "total_cost": 700000
        }
    ]
}
```

---

## Create Analysis Version

Creates a new version of an existing analysis.

```http
POST /analyses/{analysis_id}/versions
```

### Request

```json
{
    "context": "The construction site has higher transportation costs."
}
```

### Response — 202 Accepted

```json
{
    "id": "uuid",
    "parent_analysis_id": "uuid",
    "version": 2,
    "status": "processing"
}
```

---

# 9. Recommendations

## Generate Recommendations

```http
POST /analyses/{analysis_id}/recommendations
```

### Response — 202 Accepted

```json
{
    "analysis_id": "uuid",
    "status": "processing"
}
```

---

## List Analysis Recommendations

```http
GET /analyses/{analysis_id}/recommendations
```

### Response

```json
[
    {
        "id": "uuid",
        "title": "Purchase Cement in Multiple Batches",
        "description": "Purchase cement according to each construction phase to reduce storage-related losses.",
        "impact": "Estimated reduction of 8% in material waste."
    }
]
```

---

# 10. Chat

## Create Chat

```http
POST /analyses/{analysis_id}/chats
```

### Response — 201 Created

```json
{
    "id": "uuid",
    "analysis_id": "uuid",
    "created_at": "2026-08-19T10:00:00Z"
}
```

---

## List Analysis Chats

```http
GET /analyses/{analysis_id}/chats
```

---

## Get Chat Messages

```http
GET /chats/{chat_id}/messages
```

### Response

```json
[
    {
        "id": "uuid",
        "role": "user",
        "content": "What happens if I use a different cement supplier?",
        "created_at": "2026-08-19T10:00:00Z"
    },
    {
        "id": "uuid",
        "role": "assistant",
        "content": "The total estimated cost may change depending on the new unit price.",
        "created_at": "2026-08-19T10:00:05Z"
    }
]
```

---

## Send Message

```http
POST /chats/{chat_id}/messages
```

### Request

```json
{
    "content": "The cement price is now 7500 Kz."
}
```

### Response — 201 Created

```json
{
    "id": "uuid",
    "role": "user",
    "content": "The cement price is now 7500 Kz.",
    "created_at": "2026-08-19T10:00:00Z"
}
```

The assistant response may be generated asynchronously or returned directly, depending on the implementation.

---

# 11. Primary Application Flow

```text
1. Create User
        ↓
2. Create Organization
        ↓
3. Upload Construction Plan
        ↓
4. Process Plan
        ↓
5. Plan Status = ready
        ↓
6. Create Analysis
        ↓
7. Analysis Status = ready
        ↓
8. View:
   - Materials
   - Estimated Cost
   - Waste Percentage
   - CO₂ Savings
        ↓
9. Generate Recommendations
        ↓
10. Open Analysis Chat
        ↓
11. Provide Additional Context
        ↓
12. Create New Analysis Version
```

---

# 12. Final Resource Structure

```text
/users
/users/{user_id}

/users/{user_id}/organizations
/organizations
/organizations/{organization_id}

/plans/{organization_id}
/plans
/plans/{plan_id}
/plans/{plan_id}/process

/plans/{plan_id}/analyses
/analyses
/analyses/{analysis_id}
/analyses/{analysis_id}/versions

/analyses/{analysis_id}/recommendations

/analyses/{analysis_id}/chats
/chats/{chat_id}
/chats/{chat_id}/messages
```

---

# 13. Future Improvements

Future versions may introduce:

- JWT authentication;
- refresh tokens;
- persistent sessions;
- multi-user organizations;
- organization members;
- roles and permissions;
- supplier management;
- material price catalogs;
- location-based pricing;
- construction project management;
- direct PDF report generation;
- real-time analysis status;
- WebSockets;
- notifications.

The MVP intentionally prioritizes the core value proposition:

> **Receive a construction plan, analyze it, estimate the materials and cost required, identify potential waste, provide sustainability recommendations, and allow the analysis to evolve as the user provides additional context.**
