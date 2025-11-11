# TransitMCP

**Multi-Provider MCP Server for European Public Transit Information**

TransitMCP is a Model Context Protocol (MCP) server that provides real-time public transit information across Europe via the HAFAS API. Support for multiple transit providers including ÖBB (Austria), Deutsche Bahn (Germany), SBB (Switzerland), NS (Netherlands), and more.

## 🌍 Supported Transit Providers

| Provider | Country | Profile ID | Description |
|----------|---------|------------|-------------|
| **ÖBB** | 🇦🇹 Austria | `oebb` | Austrian Federal Railways |
| **Deutsche Bahn** | 🇩🇪 Germany | `db` | German Federal Railway |
| **SBB** | 🇨🇭 Switzerland | `sbb` | Swiss Federal Railways |
| **NS** | 🇳🇱 Netherlands | `ns` | Nederlandse Spoorwegen |
| **NVV** | 🇩🇪 Germany | `nvv` | Nordhessischer Verkehrsverbund |
| **VSN** | 🇩🇪 Germany | `vsn` | Verkehrsverbund Süd-Niedersachsen |

*Additional HAFAS providers can be added via configuration*

## ✨ Features

- **Multi-Provider Support**: Switch between different transit providers on the fly
- **Station Search**: Find stations by name across Europe
- **Journey Planning**: Get connections with transfers, times, and durations
- **Real-Time Departures**: Check upcoming departures from any station
- **Real-Time Arrivals**: Monitor arriving trains/buses at stations
- **Delay Information**: Get real-time delay and platform change notifications

## 📋 Requirements

- Python 3.10 or higher
- MCP-compatible client (e.g., Claude Desktop)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/StefanOOE/transit-mcp.git
cd transit-mcp
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Transit Provider

Set your default transit provider via environment variable (optional):

```bash
export TRANSIT_PROFILE=oebb  # Default is 'oebb'
# Options: oebb, db, sbb, ns, nvv, vsn
```

## ⚙️ Configuration

### Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "transit": {
      "command": "/absolute/path/to/transit-mcp/venv/bin/python",
      "args": [
        "/absolute/path/to/transit-mcp/run_server.py"
      ],
      "env": {
        "TRANSIT_PROFILE": "oebb"
      }
    }
  }
}
```

**Change the provider**: Modify `TRANSIT_PROFILE` to any supported provider ID.

## 🔧 Available Tools

### 1. `list_transit_profiles`

List all available transit provider profiles.

**Example**:
```
List all available transit providers
```

### 2. `set_transit_profile`

Switch to a different transit provider.

**Parameters**:
- `profile` (string): Profile ID (e.g., 'db', 'sbb', 'ns')

**Example**:
```
Switch to Deutsche Bahn profile
```

### 3. `search_stations`

Search for stations by name.

**Parameters**:
- `query` (string): Station name or partial name
- `max_results` (int, optional): Maximum results (default: 10)

**Example**:
```
Search for "Vienna Central Station"
```

### 4. `get_journeys`

Find connections between two stations.

**Parameters**:
- `origin` (string): Origin station name
- `destination` (string): Destination station name
- `date` (string, optional): Date in YYYY-MM-DD format
- `time` (string, optional): Time in HH:MM format
- `max_journeys` (int, optional): Maximum journeys (default: 5)

**Example**:
```
Find trains from Vienna to Salzburg tomorrow at 14:00
```

### 5. `get_departures`

Get upcoming departures from a station.

**Parameters**:
- `station` (string): Station name
- `max_departures` (int, optional): Maximum departures (default: 10)

**Example**:
```
Show departures from Amsterdam Central Station
```

### 6. `get_arrivals`

Get upcoming arrivals at a station.

**Parameters**:
- `station` (string): Station name
- `max_arrivals` (int, optional): Maximum arrivals (default: 10)

**Example**:
```
Show arrivals at Zurich HB
```

## 💡 Usage Examples

Once configured with Claude Desktop, you can ask:

### Austria (ÖBB)
- "What trains go from Vienna to Salzburg this afternoon?"
- "Show me departures from Innsbruck Hauptbahnhof"
- "Find connections from Graz to Linz tomorrow morning"

### Germany (Deutsche Bahn)
- "Trains from Berlin to Munich?"
- "Switch to Deutsche Bahn and find connections to Hamburg"
- "Departures from Frankfurt Hauptbahnhof"

### Switzerland (SBB)
- "Set profile to SBB and search for Zurich stations"
- "Trains from Geneva to Bern"
- "What time does the next train to Lucerne leave?"

### Netherlands (NS)
- "Use NS profile and find Amsterdam stations"
- "Trains from Rotterdam to Utrecht"
- "Show departures from Den Haag Centraal"

## 📁 Project Structure

```
transit-mcp/
├── src/
│   └── transitmcp/
│       ├── __init__.py       # Package initialization
│       ├── profiles.py       # Transit provider profiles
│       └── server.py         # Main MCP server
├── examples/
│   └── usage_examples.md     # Detailed usage examples
├── tests/
│   ├── __init__.py
│   └── test_server.py       # Tests
├── run_server.py            # Entry point
├── requirements.txt         # Dependencies
├── pyproject.toml          # Project metadata
├── setup.py                # Setup configuration
├── README.md               # This file
├── INSTALL.md              # Installation guide
├── CONTRIBUTING.md         # Contributing guidelines
└── CHANGELOG.md            # Version history
```

## 🔒 Technical Details

- **MCP SDK**: Official Python MCP SDK (≥1.2.0)
- **HAFAS Client**: pyhafas library (≥0.4.0)
- **Protocol**: stdio-based communication (MCP standard)
- **Architecture**: Multi-profile support with runtime switching
- **Error Handling**: Comprehensive SSL and network error handling

## ⚠️ Known Issues

### SSL Certificate Errors

Some HAFAS endpoints may encounter SSL certificate verification errors. When this occurs:

1. The server logs the error for debugging
2. Users receive helpful messages with alternatives:
   - Official provider website
   - Mobile apps
   - Customer service contacts

### Workarounds

```bash
# Update certificates
pip install --upgrade certifi

# Update pyhafas
pip install --upgrade pyhafas
```

## 🚧 Limitations

- Some providers use DB profile as fallback (pending dedicated profiles)
- Real-time data depends on HAFAS API availability
- Features may vary between providers

## 🔮 Planned Improvements

- [ ] Dedicated HAFAS profiles for each provider
- [ ] Direct HAFAS API implementation as fallback
- [ ] Enhanced SSL certificate handling
- [ ] Retry logic with exponential backoff
- [ ] Support for more European transit providers
- [ ] Fare and pricing information
- [ ] Service disruption alerts

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas for contribution:
- Additional transit provider profiles
- Improved error handling
- Documentation and examples
- Tests
- Bug fixes

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses [pyhafas](https://github.com/FahrplanDatenGarten/pyhafas) for HAFAS API access
- HAFAS is a product of [HaCon](https://www.hacon.de/) (Siemens Mobility)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/StefanOOE/transit-mcp/issues)
- **MCP Documentation**: https://modelcontextprotocol.io/
- **pyhafas Documentation**: https://pyhafas.readthedocs.io/

---

**Note**: This is an unofficial, community-maintained project. For official transit information, please use the respective provider's official website or mobile app.
