import csv
from io import StringIO
import os
import subprocess
import sys
import re


def read_csv(file):
    data = []
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data.append(row)
    return data


def read_csv_file(file_path):
    with open(file_path, "r") as file:
        return read_csv(file)


def rename_files(directory, condition):
    for filename in os.listdir(directory):
        if condition(filename):
            new_filename = (
                "new_" + filename
            )  # TODO: Define the new filename based on the condition
            os.rename(
                os.path.join(directory, filename), os.path.join(directory, new_filename)
            )


def run_linux_command(command):
    output = subprocess.run(command, stdout=subprocess.PIPE).stdout
    return output


def main(directory):
    command_output = run_linux_command(
        ["exiftool", "-q", "-csv", "-api", "LargeFileSupport=1", directory]
    )
    csv = read_csv(StringIO(command_output.decode("utf-8")))

    # print(csv)

    for row in csv:
        # print(row["SourceFile"])
        if re.search(r"[A-Za-z]{2}\d{6}.*.(MP4|mp4)", row["SourceFile"]) == None:
            continue

        print("x")

        if row["ImageSize"] == "":
            print(row)
            continue

        new_filename = (
            " ".join(
                [
                    re.sub(
                        r"^(\d+):(\d+):(\d+) (\d+):(\d+):(\d+)",
                        "\\1-\\2-\\3 \\4\\5\\6",
                        row["MediaCreateDate"],
                    ),
                    re.search(r"(GX\d+)", row["FileName"])[0],
                    row["ImageSize"],
                    str(round(float(row["VideoFrameRate"]))) + "fps",
                    row["AutoISOMin"] + "-" + row["AutoISOMax"],
                    row["ColorMode"],
                    row["Sharpness"],
                    re.match("\w+", row["FieldOfView"])[0],
                ]
            )
            + ".mp4"
        )
        print(row["FileName"], " -> ", new_filename)

        os.rename(
            os.path.join(directory, row["FileName"]),
            os.path.join(directory, new_filename),
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        main(directory)
    else:
        print("Please provide a directory path as a command line argument.")
