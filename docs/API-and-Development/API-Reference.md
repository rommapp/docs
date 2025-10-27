# API Reference

RomM provides a comprehensive REST API that allows you to programmatically interact with your RomM instance. Most API endpoints are authenticated and follow RESTful conventions.

## Interactive Documentation

RomM automatically generates interactive API documentation using OpenAPI (Swagger). You can access the interactive API docs directly from your running instance:

- **Swagger UI**: Available at `http://your-instance:3000/api/docs`
- **ReDoc**: Available at `http://your-instance:3000/api/redoc`

These interactive docs allow you to:

- Browse all available endpoints
- View request/response schemas
- Test API calls directly from your browser
- Understand authentication requirements
- Download the OpenAPI specification

## Base URL

The API base URL is typically:

```text
http://your-instance:3000/api
```

Replace `your-instance` with your actual RomM instance URL or IP address.

## Authentication

All API endpoints require authentication. RomM supports:

- **Basic HTTP Authentication** - Username and password
- **OAuth2 Password Bearer** - Token-based authentication (recommended for API usage)

When using OAuth2, you'll need to obtain a token from `/api/token` endpoint and include it in the `Authorization` header as `Bearer <token>`.

### OAuth2 Scopes

The API uses OAuth2 scopes to control access to different resources:

**Read Scopes:**

- `me.read` - View your profile
- `roms.read` - View ROMs
- `platforms.read` - View platforms
- `assets.read` - View assets
- `firmware.read` - View firmware
- `roms.user.read` - View user-rom properties
- `collections.read` - View collections
- `users.read` - View users

**Write Scopes:**

- `me.write` - Modify your profile
- `assets.write` - Modify assets
- `roms.user.write` - Modify user-rom properties
- `collections.write` - Modify collections
- `roms.write` - Modify ROMs
- `platforms.write` - Modify platforms
- `firmware.write` - Modify firmware
- `users.write` - Modify users
- `tasks.run` - Run tasks

## API Endpoints Overview

The RomM API provides comprehensive endpoints for managing all aspects of your ROM collection:

### Core Resources

- **Platforms** - Manage and configure gaming platforms
- **ROMs** - Full CRUD operations for ROM files with extensive filtering, searching, and metadata matching
- **Collections** - Create and manage ROM collections, smart collections, and virtual collections
- **Users** - User management, authentication, invite links, and profiles

### Supporting Features

- **Authentication** - OAuth2 token management, OIDC login, password resets
- **Search** - Metadata provider search for ROMs and covers
- **Tasks** - Background task management and execution
- **Assets** - Save files, states, screenshots management
- **Firmware** - Upload and manage firmware files for emulation
- **Configuration** - System configuration, platform bindings, and exclusions
- **Feeds** - Integration feeds for WebRcade and Tinfoil
- **Statistics** - System statistics and resource tracking

For complete endpoint documentation including request/response schemas, query parameters, and authentication requirements, visit the interactive API documentation at `/api/docs` or `/api/redoc` on your RomM instance.

## Example Usage

### Using cURL

```bash
# Get all libraries
curl -u username:password http://your-instance:3000/api/libraries

# Get a specific ROM
curl -u username:password http://your-instance:3000/api/roms/123

# Create a new ROM entry
curl -X POST -u username:password \
  -H "Content-Type: application/json" \
  -d '{"name": "New ROM", "platform_id": 1}' \
  http://your-instance:3000/api/roms
```

### Using Python

```python
import requests
from requests.auth import HTTPBasicAuth

# Setup authentication
auth = HTTPBasicAuth('username', 'password')
base_url = 'http://your-instance:3000/api'

# Get all libraries
response = requests.get(f'{base_url}/libraries', auth=auth)
libraries = response.json()

# Get a specific ROM
response = requests.get(f'{base_url}/roms/123', auth=auth)
rom = response.json()
```

### Using JavaScript/Node.js

```javascript
const axios = require("axios");

// Setup authentication
const api = axios.create({
    baseURL: "http://your-instance:3000/api",
    auth: {
        username: "username",
        password: "password",
    },
});

// Get all libraries
const libraries = await api.get("/libraries");

// Get a specific ROM
const rom = await api.get("/roms/123");
```

## OpenAPI Specification

You can download the complete OpenAPI specification from your RomM instance:

```text
http://your-instance:3000/api/openapi.json
```

This specification can be imported into API testing tools like Postman, used to generate client libraries, or used for API mocking.

## Getting Help

For API-specific questions or issues:

1. Check the interactive documentation at `/api/docs` or `/api/redoc` on your instance
2. Review the code in the [RomM repository](https://github.com/rommapp/romm)
3. Open an issue on [GitHub](https://github.com/rommapp/romm/issues)
4. Join the [Discord community](https://discord.com/invite/romm)
