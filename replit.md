# Overview

This is an MCP (Model Context Protocol) External API Server that provides centralized access to multiple enterprise services through a unified interface. The system integrates with Jira, Bitbucket, Confluence, and Outlook (Microsoft Graph) APIs, exposing their functionality through MCP protocol tools. It features a Python FastAPI backend server and a React TypeScript frontend dashboard for monitoring and interacting with the integrated services.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture

**MCP Protocol Server**: Built with FastAPI as the core server framework, implementing the Model Context Protocol (MCP) for tool-based API interactions. The server handles JSON-RPC 2.0 messages and provides a tool registry system for dynamic registration and execution of API operations.

**API Client Layer**: Uses a base client pattern with inheritance for each service integration. Each client (Jira, Bitbucket, Confluence, Outlook) extends a common `BaseAPIClient` that provides HTTP session management, request handling, and error management using aiohttp for async operations.

**Configuration Management**: Environment-based configuration system using dataclasses to manage API credentials, server settings, and service endpoints. All sensitive data is loaded from environment variables.

**Tool Registry System**: Dynamic tool registration and execution framework that maps MCP tool calls to specific API client methods. Supports both synchronous and asynchronous tool handlers.

## Frontend Architecture

**React TypeScript SPA**: Modern React application built with Vite for fast development and building. Uses TypeScript for type safety and better developer experience.

**Component Architecture**: Organized into service-specific panels (JiraPanel, BitbucketPanel, ConfluencePanel, OutlookPanel) with a central Dashboard component managing navigation and state.

**API Service Layer**: Centralized API communication service that handles MCP protocol messages, tool calls, and HTTP requests to the backend server.

**Responsive UI**: Bootstrap-based responsive design with service-specific color themes and Font Awesome icons for visual consistency.

## Authentication Strategy

**API Token Based**: Each service uses its native authentication method:
- Jira/Confluence: Basic auth with username + API token
- Bitbucket: Basic auth with username + app password  
- Outlook: Bearer token authentication with Microsoft Graph API

**Base64 Encoded Headers**: Authentication headers are dynamically generated using base64 encoding for basic auth services.

## Error Handling

**Layered Error Management**: Errors are handled at multiple levels - HTTP client level, API client level, and MCP protocol level. Each layer provides appropriate error transformation and logging.

**Graceful Degradation**: Frontend handles server connectivity issues with retry mechanisms and user-friendly error messages.

# External Dependencies

## Core Backend Dependencies
- **FastAPI**: Web framework for building the API server
- **aiohttp**: Async HTTP client for external API requests
- **uvicorn**: ASGI server for running the FastAPI application

## Frontend Dependencies
- **React 18**: Modern React with hooks for UI components
- **TypeScript**: Type safety and enhanced development experience
- **Vite**: Fast build tool and development server
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements

## External Service APIs
- **Jira REST API v3**: Issue tracking and project management
- **Bitbucket Cloud REST API v2.0**: Git repository management and pull requests
- **Confluence REST API**: Wiki and documentation platform
- **Microsoft Graph API v1.0**: Email and calendar services through Outlook

## Development Tools
- **ESLint**: Code linting for TypeScript/React
- **CORS Middleware**: Cross-origin request handling for development

## Service Endpoints
- Backend server runs on port 8000
- Frontend development server runs on port 5000
- Frontend proxies API requests to backend via `/api` prefix
- Health check endpoint available at `/health`