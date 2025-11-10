# Changelog

All notable changes to ScottyMCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- ÖBB-specific HAFAS profile configuration
- Trip tracking functionality
- Fare and pricing information
- Station facilities and amenities information
- Real-time platform change notifications
- Service disruption alerts

## [0.1.0] - 2025-11-10

### Added
- Initial release of ScottyMCP
- MCP server implementation using official Python SDK
- Integration with pyhafas for HAFAS API access
- Four main tools:
  - `search_stations`: Search for train stations by name
  - `get_journeys`: Find connections between stations
  - `get_departures`: Get upcoming departures from a station
  - `get_arrivals`: Get upcoming arrivals at a station
- Comprehensive documentation:
  - README with overview and usage examples
  - INSTALL guide with step-by-step instructions
  - CONTRIBUTING guidelines for developers
- Project structure with proper packaging
- Example configuration for Claude Desktop
- Apache 2.0 license
- Python 3.10+ support

### Technical Details
- Uses MCP SDK 1.2.0+
- Uses pyhafas 0.4.0+
- Stdio-based communication protocol
- Async/await support throughout

[Unreleased]: https://github.com/yourusername/ScottyMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/ScottyMCP/releases/tag/v0.1.0
