#!/usr/bin/env python3
"""
Full-Stack Python Kit GUI Application

A modern desktop application built with NiceGUI demonstrating
the GUI capabilities of the Full-Stack Python Kit.
"""

import asyncio
import json
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from nicegui import ui, app, run
import httpx


class SystemMonitor:
    """System monitoring utilities."""
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Get comprehensive system information."""
        return {
            "Platform": platform.platform(),
            "System": platform.system(),
            "Release": platform.release(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Python Version": sys.version.split()[0],
            "Python Implementation": platform.python_implementation(),
            "Current Directory": str(Path.cwd()),
            "Current Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


class APITester:
    """API testing utilities."""
    
    def __init__(self):
        self.response_data = None
        
    async def make_request(self, url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make HTTP request and return response data."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers or {})
                else:
                    raise ValueError(f"Method {method} not supported yet")
                
                result = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content": response.text,
                    "url": str(response.url),
                    "elapsed": response.elapsed.total_seconds(),
                }
                
                # Try to parse as JSON
                try:
                    result["json"] = response.json()
                except json.JSONDecodeError:
                    result["json"] = None
                
                return result
                
        except Exception as e:
            return {
                "error": str(e),
                "status_code": None,
                "headers": {},
                "content": "",
                "url": url,
                "elapsed": 0,
                "json": None,
            }


class FileExplorer:
    """File system exploration utilities."""
    
    def __init__(self):
        self.current_path = Path.cwd()
        
    def get_directory_contents(self, path: Path) -> List[Dict[str, Any]]:
        """Get directory contents with metadata."""
        if not path.exists() or not path.is_dir():
            return []
            
        items = []
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith('.'):
                    continue
                    
                stat = item.stat()
                items.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else None,
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "icon": "📁" if item.is_dir() else "📄",
                })
        except PermissionError:
            pass
            
        return items


def create_main_layout():
    """Create the main application layout."""
    
    # Initialize utilities
    system_monitor = SystemMonitor()
    api_tester = APITester()
    file_explorer = FileExplorer()
    
    # State variables
    current_tab = {"value": "dashboard"}
    
    with ui.header().classes('bg-gray-900 text-white'):
        with ui.row().classes('w-full items-center'):
            ui.icon('dashboard').classes('text-2xl mr-3')
            ui.label('Full-Stack Python Kit').classes('text-xl font-bold')
            ui.space()
            ui.label(f'Python {sys.version.split()[0]}').classes('text-sm opacity-75')
    
    with ui.footer().classes('bg-gray-800 text-white text-center'):
        ui.label('Full-Stack Python Kit - Powered by NiceGUI').classes('text-sm')
    
    # Main content area
    with ui.column().classes('flex-1 p-4'):
        
        # Tab navigation
        with ui.tabs().classes('w-full') as tabs:
            dashboard_tab = ui.tab('dashboard', label='Dashboard', icon='dashboard')
            system_tab = ui.tab('system', label='System Info', icon='computer')
            api_tab = ui.tab('api', label='API Tester', icon='http')
            files_tab = ui.tab('files', label='File Explorer', icon='folder')
            
        with ui.tab_panels(tabs, value='dashboard').classes('w-full flex-1'):
            
            # Dashboard Panel
            with ui.tab_panel('dashboard'):
                ui.label('Welcome to Full-Stack Python Kit GUI').classes('text-3xl font-bold mb-6')
                
                with ui.grid(columns=2).classes('gap-4 w-full'):
                    
                    # Quick Stats Card
                    with ui.card().classes('p-6'):
                        ui.label('Quick Stats').classes('text-xl font-semibold mb-4')
                        with ui.column().classes('gap-2'):
                            ui.label(f'🐍 Python {sys.version.split()[0]}')
                            ui.label(f'💻 {platform.system()} {platform.release()}')
                            ui.label(f'📁 {Path.cwd().name}')
                            ui.label(f'🕒 {datetime.now().strftime("%H:%M:%S")}')
                    
                    # Actions Card
                    with ui.card().classes('p-6'):
                        ui.label('Quick Actions').classes('text-xl font-semibold mb-4')
                        with ui.column().classes('gap-2'):
                            ui.button('View System Info', 
                                     on_click=lambda: tabs.set_value('system'),
                                     icon='computer').classes('w-full')
                            ui.button('Test API Endpoint', 
                                     on_click=lambda: tabs.set_value('api'),
                                     icon='http').classes('w-full')
                            ui.button('Browse Files', 
                                     on_click=lambda: tabs.set_value('files'),
                                     icon='folder').classes('w-full')
                
                # Features Overview
                with ui.card().classes('p-6 mt-6'):
                    ui.label('Features Overview').classes('text-xl font-semibold mb-4')
                    with ui.grid(columns=3).classes('gap-4'):
                        
                        with ui.column().classes('text-center'):
                            ui.icon('code').classes('text-4xl text-blue-500 mb-2')
                            ui.label('CLI Tools').classes('font-semibold')
                            ui.label('Command-line utilities built with Typer').classes('text-sm text-gray-600')
                        
                        with ui.column().classes('text-center'):
                            ui.icon('web').classes('text-4xl text-green-500 mb-2')
                            ui.label('Web Apps').classes('font-semibold')
                            ui.label('FastAPI backend with Next.js frontend').classes('text-sm text-gray-600')
                        
                        with ui.column().classes('text-center'):
                            ui.icon('desktop_windows').classes('text-4xl text-purple-500 mb-2')
                            ui.label('Desktop GUI').classes('font-semibold')
                            ui.label('Modern desktop apps with NiceGUI').classes('text-sm text-gray-600')
            
            # System Info Panel
            with ui.tab_panel('system'):
                ui.label('System Information').classes('text-2xl font-bold mb-6')
                
                system_info = system_monitor.get_system_info()
                
                with ui.card().classes('p-6'):
                    ui.label('System Details').classes('text-xl font-semibold mb-4')
                    
                    columns = [
                        {'name': 'Property', 'label': 'Property', 'field': 'property'},
                        {'name': 'Value', 'label': 'Value', 'field': 'value'},
                    ]
                    
                    rows = [{'property': k, 'value': v} for k, v in system_info.items()]
                    
                    ui.table(columns=columns, rows=rows).classes('w-full')
                
                # Real-time clock
                clock_label = ui.label().classes('text-center text-lg mt-4')
                
                def update_clock():
                    clock_label.text = f'Current Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                
                # Update clock every second
                ui.timer(1.0, update_clock)
                update_clock()  # Initial update
            
            # API Tester Panel
            with ui.tab_panel('api'):
                ui.label('API Tester').classes('text-2xl font-bold mb-6')
                
                with ui.card().classes('p-6'):
                    ui.label('HTTP Request Tester').classes('text-xl font-semibold mb-4')
                    
                    # Request form
                    with ui.row().classes('gap-4 mb-4 w-full'):
                        method_select = ui.select(['GET', 'POST', 'PUT', 'DELETE'], 
                                                value='GET').classes('w-32')
                        url_input = ui.input('URL', 
                                           value='https://httpbin.org/json',
                                           placeholder='Enter URL to test').classes('flex-1')
                    
                    # Headers input
                    headers_input = ui.textarea('Headers (JSON format)', 
                                              value='{}',
                                              placeholder='{"Authorization": "Bearer token"}').classes('w-full mb-4')
                    
                    # Response area
                    response_card = ui.card().classes('p-4 mt-4 hidden')
                    
                    async def make_api_request():
                        """Handle API request."""
                        try:
                            # Parse headers
                            headers = json.loads(headers_input.value) if headers_input.value.strip() else {}
                        except json.JSONDecodeError:
                            ui.notify('Invalid JSON in headers', type='negative')
                            return
                        
                        if not url_input.value.strip():
                            ui.notify('Please enter a URL', type='negative')
                            return
                        
                        # Show loading
                        ui.notify('Making request...', type='info')
                        
                        # Make request
                        result = await api_tester.make_request(
                            url_input.value.strip(),
                            method_select.value,
                            headers
                        )
                        
                        # Show response
                        response_card.classes(remove='hidden')
                        
                        with response_card:
                            response_card.clear()
                            
                            if 'error' in result:
                                ui.label(f'Error: {result["error"]}').classes('text-red-600 font-semibold')
                            else:
                                # Status and basic info
                                status_color = 'text-green-600' if 200 <= result['status_code'] < 300 else 'text-red-600'
                                ui.label(f'Status: {result["status_code"]}').classes(f'{status_color} font-semibold')
                                ui.label(f'Time: {result["elapsed"]:.2f}s').classes('text-gray-600')
                                
                                # Response body
                                if result['json']:
                                    ui.label('Response (JSON):').classes('font-semibold mt-4')
                                    ui.code(json.dumps(result['json'], indent=2)).classes('w-full')
                                else:
                                    ui.label('Response (Text):').classes('font-semibold mt-4')
                                    ui.code(result['content'][:1000] + ('...' if len(result['content']) > 1000 else '')).classes('w-full')
                    
                    ui.button('Send Request', 
                             on_click=make_api_request,
                             icon='send').classes('bg-blue-600 text-white')
                    
                    # Response display area (will be populated dynamically)
                    response_card
            
            # File Explorer Panel
            with ui.tab_panel('files'):
                ui.label('File Explorer').classes('text-2xl font-bold mb-6')
                
                # Current path display
                current_path_label = ui.label(f'📁 {file_explorer.current_path}').classes('text-lg mb-4')
                
                # File list container
                file_list_container = ui.column().classes('w-full')
                
                def update_file_list():
                    """Update the file list display."""
                    file_list_container.clear()
                    current_path_label.text = f'📁 {file_explorer.current_path}'
                    
                    # Parent directory button (if not root)
                    if file_explorer.current_path.parent != file_explorer.current_path:
                        with file_list_container:
                            def go_up():
                                file_explorer.current_path = file_explorer.current_path.parent
                                update_file_list()
                            
                            ui.button('📁 .. (Parent Directory)', 
                                     on_click=go_up,
                                     icon='arrow_upward').classes('w-full text-left mb-2')
                    
                    # Directory contents
                    contents = file_explorer.get_directory_contents(file_explorer.current_path)
                    
                    if not contents:
                        with file_list_container:
                            ui.label('No files or directories found').classes('text-gray-500 text-center py-8')
                        return
                    
                    # Create file/directory buttons
                    with file_list_container:
                        for item in contents:
                            def create_click_handler(item_path: str, is_dir: bool):
                                def handle_click():
                                    if is_dir:
                                        file_explorer.current_path = Path(item_path)
                                        update_file_list()
                                    else:
                                        # For files, show a notification (could be extended to open/view)
                                        ui.notify(f'Selected file: {Path(item_path).name}', type='info')
                                return handle_click
                            
                            with ui.row().classes('w-full items-center gap-2 p-2 hover:bg-gray-100 rounded'):
                                ui.label(item['icon']).classes('text-xl')
                                
                                button_text = f"{item['name']}"
                                if item['type'] == 'file' and item['size'] is not None:
                                    size_str = f" ({item['size']:,} bytes)" if item['size'] < 1024 else f" ({item['size']//1024:,} KB)"
                                    button_text += size_str
                                
                                ui.button(button_text,
                                         on_click=create_click_handler(item['path'], item['type'] == 'directory'),
                                         color=None).classes('flex-1 text-left justify-start')
                                
                                ui.label(item['modified']).classes('text-sm text-gray-500 min-w-fit')
                
                # Initial file list
                update_file_list()


def main():
    """Main application entry point."""
    
    # Configure NiceGUI
    ui.dark_mode().enable()  # Enable dark theme
    
    # Set page configuration
    app.native.window_args['resizable'] = True
    app.native.start_args['debug'] = False
    
    # Create the main layout
    create_main_layout()
    
    # Run the application
    if __name__ in {'__main__', '__mp_main__'}:
        ui.run(
            title='Full-Stack Python Kit GUI',
            native=True,
            window_size=(1200, 800),
            fullscreen=False,
            dark=True,
        )


if __name__ == '__main__':
    main()