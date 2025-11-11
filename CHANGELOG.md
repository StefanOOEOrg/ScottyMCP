# Changelog

All notable changes to TransitMCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Dedicated HAFAS profiles for each provider
- Trip tracking functionality
- Fare and pricing information
- Station facilities and amenities information
- Real-time platform change notifications
- Service disruption alerts
- Support for more European transit providers (SNCF, NMBS, DSB, etc.)

## [0.2.0] - 2025-11-10

### Major Changes
- **Project renamed** from ScottyMCP to TransitMCP for broader international appeal
- **Multi-provider support**: Can now switch between different transit providers
- **Package renamed** from `scottymcp` to `transitmcp`

### Added
- Multi-profile architecture supporting different HAFAS providers
- Six transit provider profiles: ÖBB (Austria), DB (Germany), SBB (Switzerland), NS (Netherlands), NVV, VSN
- New tool: `list_transit_profiles` - List all available providers
- New tool: `set_transit_profile` - Switch between providers at runtime
- Environment variable `TRANSIT_PROFILE` for default provider selection
- Profile-specific error messages with appropriate website links
- Comprehensive English documentation for international users
- Transit provider comparison table in README

### Changed
- All documentation translated to English
- Error messages now adapt to selected provider
- Server name from "scottymcp" to "transitmcp"
- Claude Desktop config updated to use "transit" identifier
- README completely rewritten for multi-provider context

### Technical
- New `profiles.py` module for provider configuration management
- Profile dataclass with country, language, timezone information
- Dynamic profile switching without server restart
- Improved logging with profile context

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
