import subprocess
import os
import re
import sys
import fcntl
import time
import selectors


def set_fd_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def run_sqlmap(url, crawl_level):
    # Replace with the path to SQLMap on your system
    sqlmap_path = '/usr/bin/sqlmap'  # Example: '/usr/bin/sqlmap/sqlmap.py'
    crawl_level = '--crawl=' + crawl_level

    # Command to run SQLMap with output redirection
    command = [sqlmap_path, '-u', url, '--batch', crawl_level]

    try:
        # Run SQLMap command using subprocess and capture output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        selector.register(process.stderr, selectors.EVENT_READ)

        start_time = time.time()
        timeout = 300  # Set the timeout in seconds (adjust as needed)

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                process.terminate()
                print(f"Timeout ({timeout} seconds) reached. Terminating SQLMap.")
                break

            for key, events in selector.select(timeout=1):
                if key.fileobj is process.stdout:
                    data = process.stdout.read()
                    if not data:
                        selector.unregister(process.stdout)
                    else:
                        sys.stdout.write(data)
                        sys.stdout.flush()
                elif key.fileobj is process.stderr:
                    data = process.stderr.read()
                    if not data:
                        selector.unregister(process.stderr)
                    else:
                        sys.stderr.write(data)
                        sys.stderr.flush()

            retcode = process.poll()
            if retcode is not None:
                break

        # Capture the final output
        stdout_data, stderr_data = process.communicate(timeout=1)
        if stdout_data is not None:
            sys.stdout.write(stdout_data)
        if stderr_data is not None:
            sys.stderr.write(stderr_data)

    except subprocess.CalledProcessError as e:
        # Capture and print any errors
        print("Error occurred:", e)
        print("SQLMap output:", e.output)

if __name__ == "__main__":
    # Take URL input from the user
    main_url = input("Enter the main URL to crawl with SQLMap: ")
    main_crawl_level = input("Enter the Crawl Level: ")

    # Run SQLMap with the provided URL
    run_sqlmap(main_url, main_crawl_level)

