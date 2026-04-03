                            Hestabit Training Development
                                    Week 7 - Day 4

# Natural Language SQL Question Answering System

## Introduction

Relational databases remain one of the most widely used technologies for storing and managing structured data. Despite their importance, interacting with databases typically requires familiarity with SQL, which can be a barrier for users without technical backgrounds.

Natural Language to SQL systems attempt to bridge this gap by allowing users to query databases using plain language. Instead of manually writing SQL statements, users can express their questions in natural language and rely on an AI system to generate the appropriate query.

The objective of the work performed on Day 4 was to design and implement a pipeline that converts natural language questions into SQL queries, executes those queries on a relational database, and returns the results in a readable format.

---

## Goals of the System

The primary goals of the implemented system were:

- Enable database querying through natural language
- Automate SQL query generation using a language model
- Ensure that generated queries are safe to execute
- Provide clear and structured responses based on database results

The overall system combines language model reasoning with traditional database querying mechanisms.

---

## System Architecture

The SQL question-answering pipeline follows a modular architecture composed of several processing stages.

```
User Question
↓
Database Schema Extraction
↓
Prompt Construction
↓
LLM-Based SQL Generation
↓
Query Validation
↓
SQL Execution
↓
Result Formatting
```

Each stage plays a specific role in ensuring that the system produces accurate and safe database queries.

---

## Technology Stack

The implementation relies on a combination of established tools and libraries:

- Python for application logic
- PostgreSQL as the relational database
- Ollama for running local language models
- Pandas for processing and displaying query results

Running the language model locally allows the system to operate without dependency on external APIs.

---

## Understanding the Database Schema

In order for the language model to generate correct SQL queries, it must be aware of the database structure.

The system retrieves metadata from PostgreSQL using the `information_schema.columns` view. This provides information such as:

- Table names
- Column names
- Data types

The extracted schema information is then included in the prompt provided to the language model. This helps the model understand which tables and fields are available when constructing SQL queries.

---

## SQL Query Generation

Once the schema and the user’s question are available, the system constructs a prompt that instructs the language model to generate a SQL query.

For example, given the question:

```
Show total sales by artist for 2023
```

The model may generate a query similar to:

```
SELECT a.name, SUM(s.amount)
FROM sales s
JOIN artists a ON s.artist_id = a.artist_id
WHERE EXTRACT(YEAR FROM s.sale_date) = 2023
GROUP BY a.name
```

The generated query is then passed to the validation stage before execution.

---

## Query Validation and Safety

Executing automatically generated SQL queries introduces potential risks, particularly if the queries attempt to modify or delete data.

To prevent such issues, the system includes a validation step that restricts allowed operations.

Queries containing commands such as the following are rejected:

- DELETE
- DROP
- UPDATE
- INSERT
- ALTER
- TRUNCATE

Only read-only queries beginning with `SELECT` are allowed. This ensures that the database cannot be modified through the system.

---

## Query Execution

Once validated, the SQL query is executed against the PostgreSQL database.

The system establishes a database connection and retrieves the query results. These results are loaded into a Pandas DataFrame for further processing.

Using Pandas simplifies operations such as formatting, aggregation, and display of tabular data.

---

## Result Processing and Presentation

The final step of the pipeline involves converting the query output into a readable form for the user.

Depending on the query, the system may return:

- A list of records
- Aggregated statistics
- A message indicating that no results were found

Presenting the output in a structured format helps ensure that users can easily interpret the information returned by the database.

---

## Implementation Structure

The project follows a modular source code structure designed to separate responsibilities across different components.

```
src/
├── pipelines/
│   └── sql_pipeline.py
├── generator/
│   └── sql_generator.py
└── utils/
    └── schema_loader.py
```

**SQL Pipeline**
Coordinates the full workflow from user input to result generation.

**SQL Generator**
Handles interaction with the language model and produces SQL queries based on prompts.

**Schema Loader**
Retrieves metadata from the database and prepares it for use in prompt construction.

---

## Benefits of the Approach

Natural language SQL systems offer several advantages:

- They simplify access to structured data for non-technical users.
- They enable faster exploration of datasets.
- They reduce the need for manual query writing.

These capabilities make such systems particularly valuable in environments where many users need access to database insights.

---

## Limitations and Challenges

Despite their potential, Text-to-SQL systems face several challenges:

- Natural language queries can be ambiguous.
- Complex joins and nested queries may be difficult for models to generate correctly.
- Incorrect schema interpretation can lead to invalid SQL.

Improving prompt design and incorporating validation mechanisms are important steps toward building more reliable systems.

---

### Learning Outcomes

Through the development of this pipeline, several key concepts were explored:

- Designing modular AI pipelines
- Integrating language models with relational databases
- Implementing schema-aware prompt engineering
- Ensuring safe query execution
- Processing and presenting structured data

These skills are directly applicable to modern AI-driven data analysis systems.

---
