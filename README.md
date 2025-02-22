# Intention Framework

A powerful framework for template-based content generation using language models.

## Project Structure

```
intention/
├── core/                   # Core framework functionality
│   ├── __init__.py
│   ├── client.py          # Main client interface
│   ├── template.py        # Template processing engine
│   └── types.py          # Type definitions and schemas
│
├── providers/             # LLM Provider implementations
│   ├── base.py           # Base provider interface
│   └── openai.py         # OpenAI provider implementation
│
├── processors/            # Input/Output processing
│   ├── input.py          # Input data preprocessing
│   └── output.py         # Output data post-processing
│
├── __init__.py           # Package initialization
├── demo.py               # Usage examples and demonstrations
├── exceptions.py         # Custom exception definitions
└── utils.py              # Utility functions
```

## Component Descriptions

### Core Components

- **client.py**: Provides the main entry point for applications to interact with the framework. Manages provider connections and template processing operations.
- **template.py**: Contains the core template processing functionality, including the Template class and related helper functions.
- **types.py**: Defines the type system and type hints used throughout the framework.

### Providers

- **base.py**: Defines the abstract base class that all providers must implement.
- **openai.py**: Implementation of the provider interface for OpenAI's language models.

### Processors

- **input.py**: Handles preprocessing and validation of input data before template processing.
- **output.py**: Manages post-processing and formatting of generated content.

### Utility Files

- **demo.py**: Contains example code and usage demonstrations of the framework.
- **exceptions.py**: Custom exception classes for proper error handling.
- **utils.py**: Common utility functions used throughout the framework.

## Getting Started

[Add installation and basic usage instructions here]

## License

[Add license information here] 