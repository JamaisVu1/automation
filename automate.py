from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import os
import re
import shutil

# DEMO CODE
console = Console()

def list_files(directory):
    """List all files in the given directory."""
    try:
        files = os.listdir(directory)
        table = Table(title=f"Files in [bold green]{directory}[/bold green]")
        table.add_column("File Name", style="dim")
        for file in files:
            table.add_row(file)
        console.print(table)
    except FileNotFoundError:
        console.print("[bold red]Directory not found.[/bold red]")



def move_file(directory, file, target_directory):
    """Move the given file from the current directory to the target directory."""
    try:
        shutil.move(os.path.join(directory, file), os.path.join(target_directory, file))
        console.print(f"[bold green]{file}[/bold green] has been moved from [bold blue]{directory}[/bold blue] to [bold yellow]{target_directory}[/bold yellow]")
    except FileNotFoundError:
        console.print("[bold red]Directory or file not found.[/bold red]")


def search_files(directory, pattern):
    """Search files in the given directory that match the given regex pattern."""
    try:
        files = os.listdir(directory)
        matches = [file for file in files if re.search(pattern, file)]
        table = Table(title=f"Files in [bold green]{directory}[/bold green] matching [bold blue]{pattern}[/bold blue]")
        table.add_column("Matching File Name", style="dim")
        for match in matches:
            table.add_row(match)
        console.print(table)
    except FileNotFoundError:
        console.print("[bold red]Directory not found.[/bold red]")

# GPT ASSISTED
def create_folder(directory, folder_name):
    """Create a new folder with the specified name in the given directory."""
    folder_path = os.path.join(directory, folder_name)
    
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            console.print(f"[bold green]{folder_name}[/bold green] created successfully in [bold blue]{directory}[/bold blue].")
        else:
            console.print(f"[bold yellow]{folder_name}[/bold yellow] already exists in [bold blue]{directory}[/bold blue].")
    except Exception as e:
        console.print(f"[bold red]Failed to create {folder_name} in {directory}:[/bold red] {str(e)}")


def handle_deleted_user(temp_folder_path):
    """Prompt for a deleted user's folder name and move documents to a temporary folder."""
    user_folder_name = Prompt.ask("Enter the deleted user's folder name")
    user_folder = os.path.join(os.getcwd(), user_folder_name)
    temp_folder = os.path.join(os.getcwd(), temp_folder_path)
    
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
        console.print(f"[bold green]Temporary folder {temp_folder_path} created successfully.[/bold green]")
    
    try:
        if os.path.exists(user_folder):
            for document in os.listdir(user_folder):
                document_path = os.path.join(user_folder, document)
                shutil.move(document_path, temp_folder)
            console.print(f"[bold green]All documents from {user_folder_name} have been moved to the temporary folder {temp_folder_path}.[/bold green]")
        else:
            console.print(f"[bold red]User folder {user_folder_name} does not exist.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Failed to move documents for {user_folder_name}:[/bold red] {str(e)}")

def create_folder_if_not_exists(folder_path):
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        console.print(f"[bold green]{folder_path}[/bold green] created successfully.")
        
    else:
        console.print(f"[bold yellow]{folder_path}[/bold yellow] already exists.")

def sort_documents_into_folders(directory):
  
    logs_folder = os.path.join(directory, 'logs')
    mail_folder = os.path.join(directory, 'mail')
    
    create_folder_if_not_exists(logs_folder)
    create_folder_if_not_exists(mail_folder)
    
    try:
        for file in os.listdir(directory):
            if file.endswith('.log.txt'):
                
                shutil.move(os.path.join(directory, file), os.path.join(logs_folder, file))
                
                console.print(f"[bold green]{file}[/bold green] moved to [bold blue]logs[/bold blue] folder.")
                
            elif file.endswith('.mail'):
                
                shutil.move(os.path.join(directory, file), os.path.join(mail_folder, file))
                
                console.print(f"[bold green]{file}[/bold green] moved to [bold blue]mail[/bold blue] folder.")
                
    except Exception as e:
        console.print(f"[bold red]Error sorting documents:[/bold red] {str(e)}")

# GPT ASSISTED
def parse_log_files(logs_directory, target_directory):
    
    create_folder_if_not_exists(target_directory)
    
    errors_log_path = os.path.join(target_directory, 'errors.log')
    warnings_log_path = os.path.join(target_directory, 'warnings.log')
    
    try:
        
        open(errors_log_path, 'w').close()
        open(warnings_log_path, 'w').close()
        
        for log_file in os.listdir(logs_directory):
            if log_file.endswith('.log.txt'):  
                with open(os.path.join(logs_directory, log_file), 'r') as file:
                    for line in file:
                        if 'ERROR' in line:
                            # Write error messages to errors.log
                            with open(errors_log_path, 'a') as errors_file:
                                errors_file.write(line)
                        elif 'WARNING' in line:
                            # Write warning messages to warnings.log
                            with open(warnings_log_path, 'a') as warnings_file:
                                warnings_file.write(line)
        
        console.print(f"[bold green]Log files parsed. Errors and warnings have been written to {target_directory}.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error parsing log files:[/bold red] {str(e)}")

#GPT ASSISTED
def count_file_types(directory, file_extensions):
    
    file_counts = {ext: 0 for ext in file_extensions}

    try:
        for file in os.listdir(directory):
            for ext in file_extensions:
                if file.endswith(ext):
                    file_counts[ext] += 1

        for ext, count in file_counts.items():
            console.print(f"[bold green]{ext}[/bold green] files: [bold yellow]{count}[/bold yellow]")
    except FileNotFoundError:
        console.print(f"[bold red]Directory '{directory}' not found.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error counting file types:[/bold red] {str(e)}")




def main():
    """Main function to run the CLI app."""
    while True:
        console.print("\n1. List files\n2. Move file\n3. Search files\n4. Create Folder\n5. Delete User\n6. Sort Documents\n7. Parse Logs \n8. Count File Type \n9. Exit")
        choice = Prompt.ask("Choose a task (Enter the number)", choices=['1', '2', '3', '4', '5', '6', '7','8'], default='4')

        if choice == '1':
            directory = Prompt.ask("Enter the directory to list files")
            list_files(directory)
        elif choice == '2':
            directory = Prompt.ask("Enter the current directory of the file")
            file = Prompt.ask("Enter the file to move")
            target_directory = Prompt.ask("Enter the target directory to move the file to")
            move_file(directory, file, target_directory)
        elif choice == '3':
            directory = Prompt.ask("Enter the directory to search files")
            pattern = Prompt.ask("Enter the regex pattern to search for")
            search_files(directory, pattern)
            
        elif choice == '4':
            directory = Prompt.ask("Enter the directory where the folder will be created")
            folder_name = Prompt.ask("Enter the name of the folder to create")
            create_folder(directory, folder_name)
            
        elif choice == '5':
            temp_folder_path = "temp"
            handle_deleted_user(temp_folder_path)
        
        elif choice == '6':
            directory = Prompt.ask("Enter the directory to sort documents in")
            sort_documents_into_folders(directory)
        
        elif choice == '7':
            logs_directory = Prompt.ask("Enter the logs directory")
            target_directory = Prompt.ask("Enter the target directory for errors and warnings logs")
            parse_log_files(logs_directory, target_directory)
            
        elif choice == '8':
            directory = Prompt.ask("Enter the directory to count file types in")
            file_extensions_input = Prompt.ask("Enter the file extensions to count, separated by commas (e.g., .txt,.log)")
            file_extensions = [ext.strip() for ext in file_extensions_input.split(',')]
            count_file_types(directory, file_extensions)
            
        else:
            break


if __name__ == "__main__":
    main()
    





