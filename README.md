[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/isaacwasserman-mcp-snowflake-server-badge.png)](https://mseep.ai/app/isaacwasserman-mcp-snowflake-server)

# Snowflake MCP Server

[![smithery badge](https://smithery.ai/badge/mcp_snowflake_server)](https://smithery.ai/server/mcp_snowflake_server) [![PyPI - Version](https://img.shields.io/pypi/dm/mcp-snowflake-server?color&logo=pypi&logoColor=white&label=PyPI%20downloads)](https://pypi.org/project/mcp-snowflake-server/)

---

## Overview
A Model Context Protocol (MCP) server implementation that provides database interaction with Snowflake. This server enables running SQL queries via tools and exposes data insights and schema context as resources.

---


### Installing Locally

1. Install `uv`:

`uv` is a modern package manager for Python that will handle your python environment and dependencies.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install Python 3.12 (if not already installed):

```bash
uv venv --python=3.12
```

3. Set up Cursor/Windsurf access. If you need access, request it using the `/request-access` command in Slack.

4. Ensure your Snowflake access is active. Use the `/snowflake-access` command in Slack for activation.

Note - if you had a Snowflake account but get a SAML error when logging in, run `/snowflake-access re_enable` on Slack to automatically re-enable your account

5. Open the project in your IDE and configure the MCP server

**Cursor**

Open the project in Cursor and create a directory named `.cursor` in the root of the project.

Create a file named `mcp.json` inside the `.cursor` directory and paste the following JSON configuration, updating the values as below.

**Windsurf**

Create a file named `mcp_config.json` in the root of the project and paste the following JSON configuration, updating the values as below.

```json
{
    "mcpServers": {
        "snowflake_local": {
            "command": "/Users/<macusername>/.local/bin/uv", // Replace with your actual uv path. Run `which uv` in the terminal if you don't know this
            "args": [
                "--directory",
                "/Users/macusername/projects/mcp-snowflake-server",  // Replace with your actual repo path
                "run",
                "mcp_snowflake_server",
                "--account",
                "YW26239-DELIVEROO",
                "--warehouse",
                "bi_development",
                "--user",
                "first.last@deliveroo.com",  // Replace with your email address
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

6. Test the setup by typing "list databases" in the Cursor chat. This should display all available databases. Note that a browser window will open for authentication.

### Troubleshooting

1. If the setup doesn't work, try restarting Cursor.
2. If you encounter a "no user found" error, you may need to activate your Snowflake account or create a new account.

### Netskope SSL issues

The Netskope certificate file is included in this repository at `certs/nscacert.pem` and is automatically loaded by the server. If you need to update it, download a new pem file from this guide [Netskope / SSL issues with python hitting APIs locally](https://deliveroo.atlassian.net/wiki/spaces/PS/pages/4760109122/A+SWG+Guide+for+Tech+and+Engineering#The-certificate-is-located-at:) and update the file.

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

---

## License

MIT
