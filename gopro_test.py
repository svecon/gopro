import unittest
import os
import csv
from unittest.mock import patch
from gopro import read_csv_file, rename_files


class TestGoPro(unittest.TestCase):
    def test_read_csv_file(self):
        # Create test file
        directory = "test_read_directory"
        filename = "test.csv"
        data = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
        ]
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, filename), "w") as file:
            csv_writer = csv.writer(file)
            for row in data:
                csv_writer.writerow(row)

        # Test if the function returns the expected data
        self.assertEqual(read_csv_file(os.path.join(directory, filename)), data)

        # Clean up test file
        os.remove(os.path.join(directory, filename))
        os.rmdir(directory)

    def test_rename_files(self):
        directory = "test_directory"
        condition = lambda filename: filename.endswith(".txt")
        filenames = ["file1.txt", "file2.txt", "file3.jpg", "file4.txt"]
        expected_new_filenames = [
            "new_file1.txt",
            "new_file2.txt",
            "file3.jpg",
            "new_file4.txt",
        ]

        # Create test files
        os.makedirs(directory, exist_ok=True)
        for filename in filenames:
            open(os.path.join(directory, filename), "a").close()

        # Patch os.rename to avoid actual file renaming
        with patch("os.rename") as mock_rename:
            rename_files(directory, condition)

            # Check if os.rename was called with the expected arguments
            expected_calls = [
                (
                    (
                        os.path.join(directory, filenames[i]),
                        os.path.join(directory, expected_new_filenames[i]),
                    ),
                )
                for i in range(len(filenames))
                if condition(filenames[i])
            ]
            mock_rename.assert_has_calls(expected_calls)

        # Clean up test files
        for filename in filenames:
            os.remove(os.path.join(directory, filename))
        os.rmdir(directory)


if __name__ == "__main__":
    unittest.main()
