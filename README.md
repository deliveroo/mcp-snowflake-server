[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/isaacwasserman-mcp-snowflake-server-badge.png)](https://mseep.ai/app/isaacwasserman-mcp-snowflake-server)

# Snowflake MCP Server

[![smithery badge](https://smithery.ai/badge/mcp_snowflake_server)](https://smithery.ai/server/mcp_snowflake_server) [![PyPI - Version](https://img.shields.io/pypi/dm/mcp-snowflake-server?color&logo=pypi&logoColor=white&label=PyPI%20downloads)](https://pypi.org/project/mcp-snowflake-server/)

---

## Overview
A Model Context Protocol (MCP) server implementation that provides database interaction with Snowflake. This server enables running SQL queries via tools and exposes data insights and schema context as resources.

---

## Components

### Resources

- **`memo://insights`**  
  A continuously updated memo aggregating discovered data insights.  
  Updated automatically when new insights are appended via the `append_insight` tool.

- **`context://table/{table_name}`**  
  (If prefetch enabled) Per-table schema summaries, including columns and comments, exposed as individual resources.

---

### Tools

The server exposes the following tools:

#### Query Tools

- **`read_query`**  
  Execute `SELECT` queries to read data from the database.  
  **Input:**  
  - `query` (string): The `SELECT` SQL query to execute  
  **Returns:** Query results as array of objects

- **`write_query`** (enabled only with `--allow-write`)  
  Execute `INSERT`, `UPDATE`, or `DELETE` queries.  
  **Input:**  
  - `query` (string): The SQL modification query  
  **Returns:** Number of affected rows or confirmation

- **`create_table`** (enabled only with `--allow-write`)  
  Create new tables in the database.  
  **Input:**  
  - `query` (string): `CREATE TABLE` SQL statement  
  **Returns:** Confirmation of table creation

#### Schema Tools

- **`list_databases`**  
  List all databases in the Snowflake instance.  
  **Returns:** Array of database names

- **`list_schemas`**  
  List all schemas within a specific database.  
  **Input:**  
  - `database` (string): Name of the database  
  **Returns:** Array of schema names

- **`list_tables`**  
  List all tables within a specific database and schema.  
  **Input:**  
  - `database` (string): Name of the database  
  - `schema` (string): Name of the schema  
  **Returns:** Array of table metadata

- **`describe_table`**  
  View column information for a specific table.  
  **Input:**  
  - `table_name` (string): Fully qualified table name (`database.schema.table`)  
  **Returns:** Array of column definitions with names, types, nullability, defaults, and comments

#### Analysis Tools

- **`append_insight`**  
  Add new data insights to the memo resource.  
  **Input:**  
  - `insight` (string): Data insight discovered from analysis  
  **Returns:** Confirmation of insight addition  
  **Effect:** Triggers update of `memo://insights` resource



### Installing Locally

1. The Netskope certificate file is already included in the repository at `certs/nscacert.pem`. If you need to update it, follow the [Netskope / SSL issues with python hitting APIs locally](https://deliveroo.atlassian.net/wiki/spaces/BI/pages/5260050516/Netskope+SSL+issues+with+python+hitting+APIs+locally) guide.

2. Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install Python 3.12 (if not already installed):

```bash
uv venv --python=3.12
```

4. Set up Cursor access. If you need Cursor access, request it using the `/request-access` command in Slack.

5. Ensure your Snowflake access is active and Duo authentication is disabled. Use the `/snowflake-access` command in Slack for activation and to disable Duo.

6. Once you have both Cursor and Snowflake access, open the project in Cursor and create a directory named `.cursor` in the root of the project.

7. Create a file named `mcp.json` inside the `.cursor` directory and paste the following JSON configuration, updating the values as indicated:

```json
{
    "mcpServers": {
        "snowflake_local": {
            "command": "/Users/macusername/.local/bin/uv", // Replace with your actual uv path
            "args": [
                "--directory",
                "/Users/macusername/projects/mcp-snowflake-server",  // Replace with your actual project path
                "run",
                "mcp_snowflake_server",
                "--account",
                "XXXXXXX-DELIVEROO",  // Replace with your Snowflake account (format: XXXXX-DELIVEROO)
                "--warehouse",
                "bi_development", // Replace with your default warehouse
                "--user",
                "<snowflake username>",  // Replace with your Snowflake username (email address)
                "--role",
                "SOFTWARE_ENGINEERING",
                "--database",
                "production",
                "--schema",
                "core",
                "--authenticator",
                "externalbrowser"
            ]
        }
    }
}
```

8. Test the setup by typing "list databases" in the Cursor chat. This should display all available databases. Note that a browser window will open for authentication.

#### Troubleshooting

1. If the setup doesn't work, try restarting Cursor.
2. If you encounter a "no user found" error, you may need to activate your Snowflake account or create a new account.

## License

MIT
