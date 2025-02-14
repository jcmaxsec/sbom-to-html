# sbom-to-html © 2025 by Juan C Calderon 
# Licensed under CC BY 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/
# This license requires that reusers give credit to the creator. It allows reusers to distribute, 
# remix, adapt, and build upon the material in any medium or format, even for commercial purposes.

import argparse
import importlib
import os.path
import clicolors


# main program
parser = argparse.ArgumentParser(
    prog='sbom-to-html',
    description='Generate HTML report out of SBOM Json file',
    epilog='Licence CC BY. Use it freely and please contribute https://github.com/jcmaxsec/sbom-to-html :)',
)

parser.add_argument('format', help='CycloneDx1.4, CycloneDx1.5, CycloneDx1.6 and SPDX2.3 are supported, others versions might work')
parser.add_argument('-i', '--sbom-file', default='sbom.json', help='SBOM input file (default: %(default)s)')
parser.add_argument('-o', '--html-output-file', default='sbom.html', help='HTML output file (default: %(default)s)')
parser.add_argument('-rt', '--report-template', default='report-template.html', help='HTML template file (default: %(default)s)')

# args = parser.parse_args(['spdx2.3', '-i=sbom-s2.3.json', '-o=sbom-s2.3.html'])
# args = parser.parse_args(['CycloneDx1.6', '-i=sbom-c1.6.json', '-o=sbom-c1.6.html'])
args = parser.parse_args()

# Validate arguments validity
format = args.format.lower()
if (not os.path.isfile(args.sbom_file)):
    clicolors.print_error(f'ERROR: {args.sbom_file} SBOM file does not exist')
    exit()

# Load proper SBOM processor
if (format == 'cyclonedx1.4' or format == 'cyclonedx1.5' or format == 'cyclonedx1.6'):
    m1 = importlib.import_module('cyclonedx1')
elif (format.startswith('cyclonedx')):
    clicolors.print_warning('WARNING: Unrecognized CycloneDx format, trying CycloneDx 1.x formatter, If it fails feel free to create your own processor and upload it to https://github.com/jcmaxsec/sbom-to-html')
    m1 = importlib.import_module('cyclonedx1')
elif (format == 'spdx2.3'):
    m1 = importlib.import_module('spdx2')
elif (format.startswith('spdx')):
    clicolors.print_warning('WARNING: Unrecognized SPDX format, trying SPDX 2.3 formatter, If it fails feel free to create your own processor and upload it to https://github.com/jcmaxsec/sbom-to-html')
    m1 = importlib.import_module('spdx2')
else:
    clicolors.print_error('ERROR: Unsupported SBOM format, feel free to create your own processor and upload it to https://github.com/jcmaxsec/sbom-to-html')
    exit()

success = m1.generate_html_table(args.sbom_file, args.report_template, args.html_output_file)
if (success):
    clicolors.print_success(f'SUCCESS: HTML dependency table generated: {args.html_output_file}')
