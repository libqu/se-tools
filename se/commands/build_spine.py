"""
This module implements the `se build-spine` command.
"""

import argparse

import lxml.etree as etree
import se
import se.easy_xml
import se.formatting
from se.se_epub import SeEpub


def build_spine() -> int:
	"""
	Entry point for `se build-spine`
	"""

	parser = argparse.ArgumentParser(description="Generate the <spine> element for the given Standard Ebooks source directory and write it to the ebook’s metadata file.")
	parser.add_argument("-s", "--stdout", action="store_true", help="print to stdout instead of writing to the metadata file")
	parser.add_argument("directories", metavar="DIRECTORY", nargs="+", help="a Standard Ebooks source directory")
	args = parser.parse_args()

	if args.stdout and len(args.directories) > 1:
		se.print_error("Multiple directories are only allowed without the [bash]--stdout[/] option.")
		return se.InvalidArgumentsException.code

	for directory in args.directories:
		try:
			se_epub = SeEpub(directory)
		except se.SeException as ex:
			se.print_error(ex)
			return ex.code

		if args.stdout:
			print(se_epub.generate_spine().to_string())
		else:
			for node in se_epub.metadata_dom.xpath("/package/spine"):
				node.replace_with(se_epub.generate_spine())

			with open(se_epub.metadata_file_path, "w", encoding="utf-8") as file:
				file.write(se.formatting.format_xml(se_epub.metadata_dom.to_string()))

	return 0