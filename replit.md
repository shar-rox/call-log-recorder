# Call Log Assistant

## Overview

A Flask-based web application for managing business call logs with intelligent text parsing capabilities. The system allows users to input call summaries in natural language and automatically extracts structured information like company names, contact persons, and follow-up requirements. Features include smart parsing of unstructured text input, searchable call history, and follow-up tracking functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework for lightweight web application development
- **Database**: SQLite for local data persistence with a simple schema storing call records
- **Smart Parsing**: Regular expression-based natural language processing to extract structured data from free-form text input
- **Data Model**: Single table structure with fields for company, contact, summary, date, and follow-up information

### Frontend Architecture
- **Template Engine**: Jinja2 templating integrated with Flask for server-side rendering
- **UI Design**: Simple HTML forms with inline CSS styling for a clean, functional interface
- **User Interaction**: Single-page application with form submission for data entry and search/filter capabilities

### Data Processing
- **Text Parsing Logic**: Multiple regex patterns to identify company names and contact persons from natural language summaries
- **Smart Extraction**: Filters out common words to improve accuracy of company name detection
- **Date Handling**: Automatic timestamp generation for call logging

### Search and Filter System
- **Company Search**: Text-based filtering by company name
- **Follow-up Search**: Search functionality for follow-up requirements
- **Filter Types**: Options to view all logs or filter for upcoming follow-ups only

## External Dependencies

- **Flask**: Core web framework for handling HTTP requests and responses
- **SQLite3**: Built-in Python database module for data persistence (no external database server required)
- **datetime**: Python standard library for timestamp management
- **re**: Python regular expressions module for text parsing and pattern matching

The application is designed to be self-contained with minimal external dependencies, using only standard Python libraries and the Flask framework for maximum portability and ease of deployment.