"""MCP Server for ÖBB (Austrian Federal Railways) HAFAS API."""

import logging
import ssl
from datetime import datetime
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from pyhafas import HafasClient
from pyhafas.profile import DBProfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
app = Server("scottymcp")

# Initialize HAFAS client with DB profile
# Note: ÖBB uses HAFAS but there's no dedicated ÖBB profile in pyhafas yet
# The DB profile is used as a fallback, but may have SSL certificate issues
try:
    hafas_client = HafasClient(DBProfile())
    logger.info("HAFAS client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize HAFAS client: {e}")
    hafas_client = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for ÖBB train information."""
    return [
        Tool(
            name="search_stations",
            description=(
                "Search for train stations in Austria and neighboring countries. "
                "Returns station names, IDs, and locations. "
                "Use this to find station IDs needed for journey planning."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Station name or partial name to search for (e.g., 'Wien', 'Salzburg', 'Innsbruck')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_journeys",
            description=(
                "Find train connections between two stations. "
                "Returns journey options with departure/arrival times, transfers, and durations. "
                "Use station IDs from search_stations or provide station names."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Origin station name or ID",
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination station name or ID",
                    },
                    "date": {
                        "type": "string",
                        "description": "Date for journey (YYYY-MM-DD format, optional, defaults to today)",
                    },
                    "time": {
                        "type": "string",
                        "description": "Time for journey (HH:MM format, optional, defaults to now)",
                    },
                    "max_journeys": {
                        "type": "integer",
                        "description": "Maximum number of journey options to return (default: 5)",
                        "default": 5,
                    },
                },
                "required": ["origin", "destination"],
            },
        ),
        Tool(
            name="get_departures",
            description=(
                "Get upcoming departures from a specific station. "
                "Shows train number, destination, platform, and departure time. "
                "Useful for checking live departure boards."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "station": {
                        "type": "string",
                        "description": "Station name or ID to get departures from",
                    },
                    "max_departures": {
                        "type": "integer",
                        "description": "Maximum number of departures to return (default: 10)",
                        "default": 10,
                    },
                    "products": {
                        "type": "object",
                        "description": "Filter by transport types (optional)",
                        "properties": {
                            "ice_trains": {"type": "boolean", "default": True},
                            "intercity_trains": {"type": "boolean", "default": True},
                            "regional_trains": {"type": "boolean", "default": True},
                            "suburban_trains": {"type": "boolean", "default": True},
                            "buses": {"type": "boolean", "default": True},
                        },
                    },
                },
                "required": ["station"],
            },
        ),
        Tool(
            name="get_arrivals",
            description=(
                "Get upcoming arrivals at a specific station. "
                "Shows train number, origin, platform, and arrival time. "
                "Useful for checking when trains arrive at a station."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "station": {
                        "type": "string",
                        "description": "Station name or ID to get arrivals for",
                    },
                    "max_arrivals": {
                        "type": "integer",
                        "description": "Maximum number of arrivals to return (default: 10)",
                        "default": 10,
                    },
                },
                "required": ["station"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for ÖBB train information."""
    # Check if HAFAS client is available
    if hafas_client is None:
        error_msg = (
            "⚠️ Der ÖBB HAFAS Service ist derzeit nicht verfügbar.\n\n"
            "Dies kann an SSL-Zertifikatsproblemen oder Netzwerkproblemen liegen. "
            "Bitte nutzen Sie stattdessen:\n\n"
            "- **ÖBB Website**: https://www.oebb.at\n"
            "- **ÖBB Scotty App**: Verfügbar für iOS und Android\n"
            "- **ÖBB Kundenservice**: Tel. 05-1717\n\n"
            "Technischer Hinweis: pyhafas konnte nicht initialisiert werden."
        )
        return [TextContent(type="text", text=error_msg)]

    try:
        if name == "search_stations":
            return await search_stations(arguments)
        elif name == "get_journeys":
            return await get_journeys(arguments)
        elif name == "get_departures":
            return await get_departures(arguments)
        elif name == "get_arrivals":
            return await get_arrivals(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except ssl.SSLError as e:
        logger.error(f"SSL error in tool {name}: {e}", exc_info=True)
        error_msg = (
            "⚠️ SSL-Zertifikatsfehler beim Zugriff auf die ÖBB-Datenbank.\n\n"
            "Die Verbindung zur HAFAS API konnte aufgrund von Zertifikatsproblemen "
            "nicht hergestellt werden. Bitte verwenden Sie alternativ:\n\n"
            "- **ÖBB Website**: https://www.oebb.at\n"
            "- **ÖBB Scotty App**: Für iOS und Android verfügbar\n"
            "- **ÖBB Kundenservice**: Tel. 05-1717\n\n"
            f"Technischer Fehler: {str(e)}"
        )
        return [TextContent(type="text", text=error_msg)]
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        error_msg = (
            "⚠️ Technisches Problem beim Abruf der ÖBB-Informationen.\n\n"
            "Leider konnte die Information gerade nicht abgerufen werden. "
            "Bitte versuchen Sie es über:\n\n"
            "- **ÖBB Website**: https://www.oebb.at\n"
            "- **ÖBB Scotty App**: Für iOS und Android verfügbar\n"
            "- **ÖBB Kundenservice**: Tel. 05-1717\n\n"
            f"Technischer Fehler: {str(e)}"
        )
        return [TextContent(type="text", text=error_msg)]


async def search_stations(arguments: dict) -> list[TextContent]:
    """Search for train stations."""
    query = arguments["query"]
    max_results = arguments.get("max_results", 10)

    logger.info(f"Searching for stations: {query}")

    try:
        locations = hafas_client.locations(query)

        if not locations:
            return [TextContent(type="text", text=f"No stations found for query: {query}")]

        # Format results
        results = []
        for i, location in enumerate(locations[:max_results]):
            station_info = f"**{location.name}**\n"
            station_info += f"- ID: `{location.id}`\n"

            if hasattr(location, 'lat') and location.lat and hasattr(location, 'lon') and location.lon:
                station_info += f"- Coordinates: {location.lat}, {location.lon}\n"

            if hasattr(location, 'products') and location.products:
                station_info += f"- Available products: {location.products}\n"

            results.append(station_info)

        result_text = f"Found {len(results)} station(s) for '{query}':\n\n" + "\n".join(results)
        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        logger.error(f"Error searching stations: {e}")
        return [TextContent(type="text", text=f"Error searching stations: {str(e)}")]


async def get_journeys(arguments: dict) -> list[TextContent]:
    """Get journey connections between two stations."""
    origin = arguments["origin"]
    destination = arguments["destination"]
    date_str = arguments.get("date")
    time_str = arguments.get("time")
    max_journeys = arguments.get("max_journeys", 5)

    logger.info(f"Getting journeys from {origin} to {destination}")

    try:
        # Parse date and time if provided
        dt = None
        if date_str or time_str:
            date_part = date_str if date_str else datetime.now().strftime("%Y-%m-%d")
            time_part = time_str if time_str else datetime.now().strftime("%H:%M")
            dt = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")

        # Get locations for origin and destination
        origin_locations = hafas_client.locations(origin)
        dest_locations = hafas_client.locations(destination)

        if not origin_locations:
            return [TextContent(type="text", text=f"Origin station not found: {origin}")]
        if not dest_locations:
            return [TextContent(type="text", text=f"Destination station not found: {destination}")]

        origin_id = origin_locations[0].id
        dest_id = dest_locations[0].id

        # Get journeys
        journeys = hafas_client.journeys(
            origin=origin_id,
            destination=dest_id,
            date=dt,
            max_journeys=max_journeys
        )

        if not journeys:
            return [TextContent(
                type="text",
                text=f"No journeys found from {origin_locations[0].name} to {dest_locations[0].name}"
            )]

        # Format results
        results = []
        for i, journey in enumerate(journeys[:max_journeys]):
            journey_info = f"### Journey {i + 1}\n"
            journey_info += f"**Departure:** {journey.departure} from {journey.origin.name}\n"
            journey_info += f"**Arrival:** {journey.arrival} at {journey.destination.name}\n"
            journey_info += f"**Duration:** {journey.duration}\n"
            journey_info += f"**Transfers:** {journey.transfers}\n"

            if journey.legs:
                journey_info += f"\n**Legs:**\n"
                for j, leg in enumerate(journey.legs):
                    journey_info += f"{j + 1}. {leg.name or 'Transfer'}: "
                    journey_info += f"{leg.origin.name} → {leg.destination.name}\n"
                    if hasattr(leg, 'departure') and leg.departure:
                        journey_info += f"   Departs: {leg.departure}\n"
                    if hasattr(leg, 'arrival') and leg.arrival:
                        journey_info += f"   Arrives: {leg.arrival}\n"

            results.append(journey_info)

        result_text = f"Found {len(results)} journey(ies) from **{origin_locations[0].name}** to **{dest_locations[0].name}**:\n\n"
        result_text += "\n---\n\n".join(results)
        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        logger.error(f"Error getting journeys: {e}")
        return [TextContent(type="text", text=f"Error getting journeys: {str(e)}")]


async def get_departures(arguments: dict) -> list[TextContent]:
    """Get departures from a station."""
    station = arguments["station"]
    max_departures = arguments.get("max_departures", 10)

    logger.info(f"Getting departures from: {station}")

    try:
        # Get station location
        locations = hafas_client.locations(station)
        if not locations:
            return [TextContent(type="text", text=f"Station not found: {station}")]

        station_id = locations[0].id
        station_name = locations[0].name

        # Get departures
        departures = hafas_client.departures(
            station=station_id,
            date=datetime.now(),
            max_trips=max_departures
        )

        if not departures:
            return [TextContent(type="text", text=f"No departures found for {station_name}")]

        # Format results
        results = []
        results.append(f"# Departures from {station_name}\n")

        for departure in departures[:max_departures]:
            dep_info = f"**{departure.name}** to {departure.direction}\n"
            dep_info += f"- Departure: {departure.departure}\n"

            if hasattr(departure, 'platform') and departure.platform:
                dep_info += f"- Platform: {departure.platform}\n"

            if hasattr(departure, 'delay') and departure.delay:
                dep_info += f"- Delay: {departure.delay} minutes\n"

            results.append(dep_info)

        result_text = "\n".join(results)
        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        logger.error(f"Error getting departures: {e}")
        return [TextContent(type="text", text=f"Error getting departures: {str(e)}")]


async def get_arrivals(arguments: dict) -> list[TextContent]:
    """Get arrivals at a station."""
    station = arguments["station"]
    max_arrivals = arguments.get("max_arrivals", 10)

    logger.info(f"Getting arrivals at: {station}")

    try:
        # Get station location
        locations = hafas_client.locations(station)
        if not locations:
            return [TextContent(type="text", text=f"Station not found: {station}")]

        station_id = locations[0].id
        station_name = locations[0].name

        # Get arrivals
        arrivals = hafas_client.arrivals(
            station=station_id,
            date=datetime.now(),
            max_trips=max_arrivals
        )

        if not arrivals:
            return [TextContent(type="text", text=f"No arrivals found for {station_name}")]

        # Format results
        results = []
        results.append(f"# Arrivals at {station_name}\n")

        for arrival in arrivals[:max_arrivals]:
            arr_info = f"**{arrival.name}** from {arrival.origin.name if hasattr(arrival, 'origin') else 'unknown'}\n"
            arr_info += f"- Arrival: {arrival.arrival}\n"

            if hasattr(arrival, 'platform') and arrival.platform:
                arr_info += f"- Platform: {arrival.platform}\n"

            if hasattr(arrival, 'delay') and arrival.delay:
                arr_info += f"- Delay: {arrival.delay} minutes\n"

            results.append(arr_info)

        result_text = "\n".join(results)
        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        logger.error(f"Error getting arrivals: {e}")
        return [TextContent(type="text", text=f"Error getting arrivals: {str(e)}")]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
