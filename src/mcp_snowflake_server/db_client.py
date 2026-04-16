import asyncio
import logging
import uuid
from typing import Any

from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSessionException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("mcp_snowflake_server")


class SnowflakeDB:
    def __init__(self, connection_config: dict):
        self.connection_config = connection_config
        self.session = None
        self.insights: list[str] = []
        self.init_task = None  # To store the task reference

    async def _init_database(self):
        """Initialize connection to the Snowflake database"""
        try:
            # Create session without setting specific database and schema
            self.session = Session.builder.configs(self.connection_config).create()

            # Set initial warehouse if provided, but don't set database or schema
            if "warehouse" in self.connection_config:
                self.session.sql(
                    f"USE WAREHOUSE {self.connection_config['warehouse'].upper()}"
                ).collect()
        except Exception as e:
            raise ValueError(f"Failed to connect to Snowflake database: {e}")

    def start_init_connection(self):
        """Start database initialization in the background"""
        # Create a task that runs in the background
        loop = asyncio.get_event_loop()
        self.init_task = loop.create_task(self._init_database())
        return self.init_task

    async def _ensure_session(self):
        """Ensure we have a valid session, waiting for init or creating one as needed."""
        if self.init_task:
            if not self.init_task.done():
                await self.init_task
            else:
                self.init_task.result()
        if not self.session:
            await self._init_database()

    def _run_query(self, query: str) -> tuple[list[dict[str, Any]], str]:
        result = self.session.sql(query).to_pandas()
        result_rows = result.to_dict(orient="records")
        data_id = str(uuid.uuid4())
        return result_rows, data_id

    async def execute_query(self, query: str) -> tuple[list[dict[str, Any]], str]:
        """Execute a SQL query and return results as a list of dictionaries"""
        await self._ensure_session()

        logger.debug(f"Executing query: {query}")
        try:
            return self._run_query(query)

        except SnowparkSessionException:
            logger.warning("Session expired, re-authenticating...")
            self.session = None
            await self._init_database()
            return self._run_query(query)

        except Exception as e:
            logger.error(f'Database error executing "{query}": {e}')
            raise

    def add_insight(self, insight: str) -> None:
        """Add a new insight to the collection"""
        self.insights.append(insight)

    def get_memo(self) -> str:
        """Generate a formatted memo from collected insights"""
        if not self.insights:
            return "No data insights have been discovered yet."

        memo = "📊 Data Intelligence Memo 📊\n\n"
        memo += "Key Insights Discovered:\n\n"
        memo += "\n".join(f"- {insight}" for insight in self.insights)

        if len(self.insights) > 1:
            memo += f"\n\nSummary:\nAnalysis has revealed {len(self.insights)} key data insights that suggest opportunities for strategic optimization and growth."

        return memo
