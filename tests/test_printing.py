import unittest
from unittest.mock import patch, MagicMock
import subprocess
import platform
from src.print_cli.printing import get_printers, print_file

class TestPrinting(unittest.TestCase):
    
    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_get_printers_linux(self, mock_check_output, mock_platform):
        mock_platform.return_value = "Linux"
        mock_check_output.return_value = "Printer1 accepting requests since Mon Jan 1 00:00:00 2024\n"
        printers = get_printers()
        self.assertEqual(printers, ["Printer1"])
        mock_check_output.assert_called_with(["lpstat", "-a"], text=True)

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_get_printers_windows(self, mock_check_output, mock_platform):
        mock_platform.return_value = "Windows"
        mock_check_output.return_value = "PDFPrinter\nMicrosoft Print to PDF\n"
        printers = get_printers()
        self.assertEqual(printers, ["PDFPrinter", "Microsoft Print to PDF"])
        mock_check_output.assert_called_with(["powershell", "-Command", "Get-Printer | Select-Object -ExpandProperty Name"], text=True)

    @patch('platform.system')
    @patch('subprocess.check_call')
    @patch('os.path.abspath')
    def test_print_file_linux(self, mock_abspath, mock_check_call, mock_platform):
        mock_platform.return_value = "Linux"
        mock_abspath.return_value = "/absolute/test.pdf"
        success = print_file("test.pdf", "Printer1", 2)
        self.assertTrue(success)
        mock_check_call.assert_called_once_with(["lp", "-d", "Printer1", "-n", "2", "/absolute/test.pdf"])

    @patch('platform.system')
    @patch('subprocess.check_call')
    @patch('os.path.abspath')
    def test_print_file_windows(self, mock_abspath, mock_check_call, mock_platform):
        mock_platform.return_value = "Windows"
        mock_abspath.return_value = "C:\\test.pdf"
        success = print_file("test.pdf", "Printer1", 1)
        self.assertTrue(success)
        cmd = ["powershell", "-Command", "Start-Process -FilePath 'C:\\test.pdf' -Verb PrintTo -ArgumentList 'Printer1' -PassThru"]
        mock_check_call.assert_called_once_with(cmd)

if __name__ == '__main__':
    unittest.main()
