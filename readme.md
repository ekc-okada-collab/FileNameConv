# FileNameConv

A Python utility for batch renaming files in a directory.

## Features

- Rename files based on custom patterns
- Supports multiple file types
- Easy to use command-line interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python filenameconv.py <directory> [options]
```

### Options

- `--pattern <pattern>`: Specify renaming pattern
- `--preview`: Preview changes without renaming

## Example

```bash
python filenameconv.py ./files --pattern "{index}_{original}"
```

## License

MIT License