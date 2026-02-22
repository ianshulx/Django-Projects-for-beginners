#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    
    # Environment থেকে settings module নেওয়া হচ্ছে, না থাকলে default ব্যবহার হবে
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'web_crawler.settings')
    
    # Settings module টি environment variable এ set করা হচ্ছে
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    # Startup এ কিছু useful তথ্য print করা হচ্ছে
    print(f"[*] Using settings: {settings_module}")   # কোন settings file ব্যবহার হচ্ছে
    print(f"[*] Python version: {sys.version}")       # Python এর version
    print(f"[*] Django management starting...\n")     # Management command শুরু হচ্ছে

    try:
        # Django এর management module import করা হচ্ছে
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Django install না থাকলে বা virtual environment active না থাকলে error দেখাবে
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Command line arguments দিয়ে Django management command execute করা হচ্ছে
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Script সরাসরি run করলে main() function call হবে
    main()