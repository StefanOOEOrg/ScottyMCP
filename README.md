# ScottyMCP

MCP Server for ÖBB (Austrian Federal Railways) providing real-time train schedules, station information, and connection data.

## Overview

ScottyMCP is a Model Context Protocol (MCP) server that provides access to Austrian Federal Railways (ÖBB) data through the HAFAS API. It allows AI assistants like Claude to search for train stations, plan journeys, check departures and arrivals, all in real-time.

## Features

- **Station Search**: Find train stations by name across Austria and neighboring countries
- **Journey Planning**: Get train connections between stations with detailed schedules
- **Departures**: Check upcoming departures from any station
- **Arrivals**: Monitor arriving trains at stations
- **Real-time Data**: Access current timetables and delay information

## Requirements

- Python 3.10 or higher
- MCP-compatible client (e.g., Claude Desktop)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ScottyMCP.git
cd ScottyMCP
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e .
```

## Configuration

### Claude Desktop

To use ScottyMCP with Claude Desktop, add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "scottymcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/ScottyMCP/run_server.py"
      ]
    }
  }
}
```

Replace `/absolute/path/to/ScottyMCP/` with the actual path to your ScottyMCP installation.

### Other MCP Clients

For other MCP clients, use the following command to start the server:

```bash
python run_server.py
```

## Available Tools

### search_stations

Search for train stations by name.

**Parameters:**
- `query` (string, required): Station name or partial name
- `max_results` (integer, optional): Maximum number of results (default: 10)

**Example:**
```
Search for "Wien Hauptbahnhof"
```

### get_journeys

Find train connections between two stations.

**Parameters:**
- `origin` (string, required): Origin station name or ID
- `destination` (string, required): Destination station name or ID
- `date` (string, optional): Journey date in YYYY-MM-DD format
- `time` (string, optional): Journey time in HH:MM format
- `max_journeys` (integer, optional): Maximum journeys to return (default: 5)

**Example:**
```
Find connections from "Wien" to "Salzburg" at 14:00
```

### get_departures

Get upcoming departures from a station.

**Parameters:**
- `station` (string, required): Station name or ID
- `max_departures` (integer, optional): Maximum departures to return (default: 10)

**Example:**
```
Show departures from "Innsbruck Hauptbahnhof"
```

### get_arrivals

Get upcoming arrivals at a station.

**Parameters:**
- `station` (string, required): Station name or ID
- `max_arrivals` (integer, optional): Maximum arrivals to return (default: 10)

**Example:**
```
Show arrivals at "Graz Hauptbahnhof"
```

## Usage Examples

Once configured with Claude Desktop, you can ask questions like:

- "What trains go from Vienna to Salzburg this afternoon?"
- "When is the next train from Innsbruck?"
- "Show me departures from Linz Hauptbahnhof"
- "Find connections from Graz to Klagenfurt tomorrow at 9am"

## Development

### Project Structure

```
ScottyMCP/
├── src/
│   └── scottymcp/
│       ├── __init__.py
│       └── server.py          # Main MCP server implementation
├── run_server.py              # Entry point
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project metadata
├── setup.py                  # Setup configuration
└── README.md                 # This file
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

## Technical Details

- **MCP SDK**: Uses the official Python MCP SDK (mcp >= 1.2.0)
- **HAFAS Client**: Uses pyhafas for accessing HAFAS APIs
- **Protocol**: Communicates via stdio as per MCP specification
- **Transport Types**: Supports trains, buses, and other public transport

## Limitations

- Currently uses DB (Deutsche Bahn) profile as ÖBB-specific profile may need adjustment
- Real-time data depends on HAFAS API availability
- Some features may vary based on the HAFAS backend configuration

## Known Issues

### SSL Certificate Errors

The server may encounter SSL certificate verification errors when connecting to the HAFAS API. This is a known issue with some HAFAS endpoints. When this occurs, the server will:

1. Log the error for debugging
2. Return a helpful message directing users to alternative resources:
   - ÖBB Website: https://www.oebb.at
   - ÖBB Scotty App (iOS/Android)
   - ÖBB Customer Service: 05-1717

### Workarounds

If you encounter SSL errors, you can try:

1. **Update certificates**:
   ```bash
   pip install --upgrade certifi
   ```

2. **Check for pyhafas updates**:
   ```bash
   pip install --upgrade pyhafas
   ```

3. **Use alternative ÖBB services**: The official ÖBB website and mobile apps provide the same information

### Future Improvements

- Implement a dedicated ÖBB HAFAS profile
- Add direct HAFAS API implementation as fallback
- Improve SSL certificate handling
- Add retry logic with exponential backoff

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses [pyhafas](https://github.com/FahrplanDatenGarten/pyhafas) for HAFAS API access
- Inspired by the oebb-hafas JavaScript library

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [MCP documentation](https://modelcontextprotocol.io/)
- Review the [pyhafas documentation](https://pyhafas.readthedocs.io/)
