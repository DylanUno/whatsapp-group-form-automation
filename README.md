# WhatsApp Group Form Manager

A Python automation tool for managing WhatsApp group participants using phone numbers from Google Forms CSV exports. This tool streamlines the process of adding multiple participants to WhatsApp groups while maintaining compliance with WhatsApp's automation policies.

## Key Features

- Processes phone numbers from Google Forms CSV exports
- Automatically cleans and validates phone numbers
- Handles Indonesian phone number format (08 -> +628)
- Processes numbers in policy-compliant batches of 25
- Identifies invalid numbers for manual processing
- Provides detailed logging and progress tracking
- Maintains automation policy compliance through controlled timing

## WhatsApp Policy Compliance

This tool is designed to work within WhatsApp's automation policies by:
- Processing numbers in small batches (25 numbers per batch)
- Including mandatory pauses between actions
- Requiring manual confirmation between batches
- Maintaining reasonable delays between operations
- Requiring manual QR code scanning and group selection

## Prerequisites

- Python 3.7+
- Chrome browser
- Active WhatsApp account
- Access to WhatsApp Web

## Installation

1. Clone this repository:
```bash
git [clone https://github.com/yourusername/whatsapp-group-form-manager.git](https://github.com/DylanUno/whatsapp-group-form-automation.git)
cd whatsapp-group-form-automation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Export your Google Form responses as CSV
2. Update the CSV file path in the script:
```python
CSV_FILE_PATH = "your_file.csv"
```

3. Run the script:
```bash
python auto-add.py
```

4. Follow the prompts:
   - Scan the WhatsApp Web QR code
   - Navigate to your target WhatsApp group
   - Confirm each batch of 25 numbers
   - Process any invalid numbers manually

## CSV File Format

The script expects a CSV file exported from Google Forms with the following characteristics:

### Input Format Requirements
- CSV export from Google Forms responses
- Comma-separated values
- Phone numbers in the fourth column (index 3)
- First row contains headers (automatically skipped)

### Example CSV Format
```csv
Timestamp,Name,Email,Phone Number,Other Fields...
2024-01-01 10:00:00,John Doe,john@example.com,+6281234567890,...
2024-01-01 10:05:00,Jane Smith,jane@example.com,08123456789,...
```

## Invalid Number Handling

The script automatically identifies and reports invalid phone numbers that require manual processing. These include:
- Numbers containing letters
- Numbers in incorrect formats
- Numbers missing country codes
- Malformed numbers

Invalid numbers are displayed at the start of processing so you can:
1. Review them for common formatting issues
2. Add them to the group manually
3. Contact the form submitters for correct numbers if needed

## Batch Processing

To comply with WhatsApp's automation policies and prevent potential blocks:
- Numbers are processed in batches of 25
- Each batch requires manual confirmation
- Appropriate delays are maintained between actions
- Progress is clearly displayed for each batch

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is designed to work within WhatsApp's automation policies and terms of service. Please ensure you:
- Have permission to add numbers to your WhatsApp group
- Comply with WhatsApp's terms of service
- Follow local privacy laws and regulations
- Use the tool responsibly and within reasonable limits