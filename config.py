"""
Configuration management for MCP Server
Handles environment variables and settings
"""

import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration class for MCP Server"""
    
    # Jira Configuration
    jira_url: str
    jira_username: str  
    jira_api_token: str
    
    # Bitbucket Configuration
    bitbucket_username: str
    bitbucket_app_password: str
    
    # Confluence Configuration
    confluence_url: str
    confluence_username: str
    confluence_api_token: str
    
    # Outlook/Microsoft Graph Configuration
    outlook_access_token: str
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        
        # Jira settings
        self.jira_url = os.getenv("JIRA_URL", "")
        self.jira_username = os.getenv("JIRA_USERNAME", "")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN", "")
        
        # Bitbucket settings
        self.bitbucket_username = os.getenv("BITBUCKET_USERNAME", "")
        self.bitbucket_app_password = os.getenv("BITBUCKET_APP_PASSWORD", "")
        
        # Confluence settings
        self.confluence_url = os.getenv("CONFLUENCE_URL", "")
        self.confluence_username = os.getenv("CONFLUENCE_USERNAME", "")
        self.confluence_api_token = os.getenv("CONFLUENCE_API_TOKEN", "")
        
        # Outlook/Microsoft Graph settings
        self.outlook_access_token = os.getenv("OUTLOOK_ACCESS_TOKEN", "")
        
        # Server settings
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Validate required settings
        self._validate_config()
    
    def _validate_config(self):
        """Validate that required configuration is present"""
        errors = []
        
        # Check Jira config
        if not self.jira_url:
            errors.append("JIRA_URL is required")
        if not self.jira_username:
            errors.append("JIRA_USERNAME is required")
        if not self.jira_api_token:
            errors.append("JIRA_API_TOKEN is required")
        
        # Check Bitbucket config
        if not self.bitbucket_username:
            errors.append("BITBUCKET_USERNAME is required")
        if not self.bitbucket_app_password:
            errors.append("BITBUCKET_APP_PASSWORD is required")
        
        # Check Confluence config
        if not self.confluence_url:
            errors.append("CONFLUENCE_URL is required")
        if not self.confluence_username:
            errors.append("CONFLUENCE_USERNAME is required")
        if not self.confluence_api_token:
            errors.append("CONFLUENCE_API_TOKEN is required")
        
        # Check Outlook config
        if not self.outlook_access_token:
            errors.append("OUTLOOK_ACCESS_TOKEN is required")
        
        if errors:
            print("Configuration errors found:")
            for error in errors:
                print(f"  - {error}")
            print("\nPlease check your environment variables or .env file")
            # Don't exit here - allow the application to start and show meaningful errors
    
    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        return all([
            self.jira_url,
            self.jira_username,
            self.jira_api_token,
            self.bitbucket_username,
            self.bitbucket_app_password,
            self.confluence_url,
            self.confluence_username,
            self.confluence_api_token,
            self.outlook_access_token
        ])
