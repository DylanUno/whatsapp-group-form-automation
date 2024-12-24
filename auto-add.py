"""
WhatsApp Group Form Automation
=============================
A Python automation tool for managing WhatsApp group participants using Google Forms CSV exports.
This script processes numbers in policy-compliant batches and identifies invalid numbers for manual processing.

Author: Dylan Uno Syahfaril
License: MIT
"""

import time
import csv
from typing import Tuple, List, Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class ProcessedData:
    """Data structure to hold processed phone numbers and related information."""
    valid_numbers: List[str]
    invalid_numbers: List[str]
    original_numbers: List[Tuple[str, str]]  # (original, cleaned) pairs


def clean_phone_number(number: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Clean and validate a phone number to ensure proper WhatsApp format.
    
    Args:
        number (str): Raw phone number to clean and validate
    
    Returns:
        Tuple[Optional[str], Optional[str]]: Cleaned number and original number if changed
    """
    original_number = number.strip()
    number = original_number

    # Check for letters
    if any(char.isalpha() for char in number):
        return None, original_number

    # Clean the number
    number = ''.join(filter(lambda x: x.isdigit() or x == "+", 
                          number.replace(" ", "")
                                .replace("-", "")
                                .replace("(", "")
                                .replace(")", "")))

    # Handle Indonesian format (08 -> +628)
    if number.startswith("08"):
        number = "+628" + number[2:]

    # Validate international format
    if number.startswith("+") and number[1:].isdigit():
        if number != original_number:
            return number, original_number
        else:
            return number, None
    return None, original_number


def process_csv(file_path: str) -> ProcessedData:
    """
    Process a CSV file from Google Forms containing phone numbers.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        ProcessedData: Processed numbers and validation results
    """
    valid_numbers = []
    invalid_numbers = []
    original_numbers = []

    try:
        with open(file_path, "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            
            for row_num, row in enumerate(reader, start=2):
                if len(row) >= 4:
                    raw_number = row[3].strip()  # Phone number is in the 4th column
                    cleaned_number, original = clean_phone_number(raw_number)
                    
                    if cleaned_number:
                        valid_numbers.append(cleaned_number)
                        if original:
                            original_numbers.append((original, cleaned_number))
                    else:
                        invalid_numbers.append(f"Row {row_num}: {raw_number}")
                else:
                    print(f"Warning: Row {row_num} has insufficient columns")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        raise
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")
        raise

    return ProcessedData(valid_numbers, invalid_numbers, original_numbers)


def process_whatsapp_group(processed_data: ProcessedData, batch_size: int = 25, start_batch: int = 1):
    """
    Process phone numbers through WhatsApp Web interface.
    
    Args:
        processed_data (ProcessedData): Processed phone number data
        batch_size (int): Numbers per batch (default: 25 for policy compliance)
        start_batch (int): Starting batch number
    """
    # Remove duplicates while preserving order
    valid_numbers = list(dict.fromkeys(processed_data.valid_numbers))
    
    # Print processing summary
    print("\n=== Processing Summary ===")
    print(f"Total valid numbers: {len(valid_numbers)}")
    print(f"Total invalid numbers: {len(processed_data.invalid_numbers)}")
    print(f"Batch size: {batch_size}")
    print(f"Total batches: {(len(valid_numbers) + batch_size - 1) // batch_size}")
    
    # Display invalid numbers for manual processing
    if processed_data.invalid_numbers:
        print("\n=== Invalid Numbers (Require Manual Processing) ===")
        print("The following numbers could not be processed automatically:")
        for invalid in processed_data.invalid_numbers:
            print(f"  • {invalid}")
        print("\nPlease add these numbers manually after the automation completes.")
        input("Press Enter to continue with automatic processing...")

    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Start WhatsApp Web session
        driver.get('https://web.whatsapp.com')
        print("\n=== WhatsApp Web Setup ===")
        input("1. Scan the QR code and press Enter to continue...")
        input("2. Navigate to your target group and press Enter to start...")

        # Locate search box
        print("\nLocating interface elements...")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[1]/div/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/p'
            ))
        )

        # Process in batches
        total_numbers = len(valid_numbers)
        for batch_start in range((start_batch - 1) * batch_size, total_numbers, batch_size):
            batch_end = min(batch_start + batch_size, total_numbers)
            batch_numbers = valid_numbers[batch_start:batch_end]
            current_batch = batch_start // batch_size + 1
            total_batches = (total_numbers + batch_size - 1) // batch_size
            
            print(f"\n=== Processing Batch {current_batch}/{total_batches} ===")
            print(f"Numbers {batch_start + 1} to {batch_end} of {total_numbers}")

            for idx, number in enumerate(batch_numbers, 1):
                try:
                    print(f"Processing {idx}/{len(batch_numbers)}: {number}")
                    search_box.click()
                    time.sleep(1)
                    search_box.send_keys(number)
                    time.sleep(2)
                    search_box.send_keys(Keys.ENTER)
                    time.sleep(1)
                    search_box.send_keys(Keys.COMMAND + "a")
                    time.sleep(1)
                    search_box.send_keys(Keys.DELETE)
                    time.sleep(1)
                except Exception as e:
                    print(f"Error processing number {number}: {str(e)}")

            print(f"\nBatch {current_batch} completed.")
            if batch_end < total_numbers:
                input("Press Enter to continue to next batch...")

    except Exception as e:
        print(f"\nError during processing: {str(e)}")
    
    finally:
        print("\nClosing browser...")
        driver.quit()


def main():
    """Main execution function."""
    # Configuration
    CSV_FILE_PATH = "DataDigitalTalentHub.csv"
    BATCH_SIZE = 25
    START_BATCH = 1

    print("=== WhatsApp Group Form Automation ===")
    print(f"Processing CSV file: {CSV_FILE_PATH}")

    try:
        # Process CSV file
        processed_data = process_csv(CSV_FILE_PATH)
        
        # Process through WhatsApp
        process_whatsapp_group(processed_data, BATCH_SIZE, START_BATCH)
        
        print("\n=== Process Completed ===")
        if processed_data.invalid_numbers:
            print("\nReminder: Don't forget to process the invalid numbers manually!")

    except Exception as e:
        print(f"\nProgram terminated due to error: {str(e)}")
        print("Please check the error message above and try again.")


if __name__ == "__main__":
    main()