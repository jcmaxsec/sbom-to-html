# sbom-to-html © 2025 by Juan C Calderon 
# Licensed under CC BY 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/
# This license requires that reusers give credit to the creator. It allows reusers to distribute, 
# remix, adapt, and build upon the material in any medium or format, even for commercial purposes.

import json
import re
import datetime
import clicolors


def generate_html_table(sbom_file, report_template_file, output_html):
    # Get SBOM Data
    with open(sbom_file, 'r') as file:
        try:
            data = json.load(file)
        except ValueError:      # Json error exit
            clicolors.print_error('ERROR: Unable to parse sbom file: ' + sbom_file)
            return
    components = data.get('components', [])
    metadata = data.get('metadata', {})
    metadata_component = metadata.get('component', {})
    dependencies = {dep['ref']: dep.get('dependsOn', []) for dep in data.get('dependencies', [])}

    if metadata_component:
        components.insert(0, metadata_component)
    
    # Read simple template file
    with open(report_template_file, 'r') as file:
        html_content = file.read()

    # Get Scan time for report
    timestamp = metadata.get('timestamp', 'Unknown')
    if (timestamp != 'Unknown'):
        time_zone = datetime.datetime.now().astimezone().tzinfo
        scan_time = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').astimezone(time_zone).strftime('%b %d %Y, %I:%M:%S %p %Z')
    else:
        scan_time = timestamp
    # Get App name and version for report
    app_name = metadata_component.get('name', 'Application')
    app_version = metadata_component.get('version', 'N/A')

    # Get Dependency summary for report
    summary = f'<b> {len(components)}</b> dependencies found'
    
    # Generate Dependency Table for report
    chart_edges = []
    html_dep_table_rows = ''
    for i, component in enumerate(components):
        name = component.get('name', 'N/A')
        version = component.get('version', 'N/A')
        licenses = ', '.join(lic.get('expression', 'Unknown') for lic in component.get('licenses', []))
        purl = component.get('purl', 'N/A')
        depends_on = dependencies.get(component.get('bom-ref', ''), [])
        subdeps = '<ul>'
        for dep in depends_on:
            subdep_name = re.search(r'-([^@]+@.*)', dep).group(1)
            subdeps += '<li>' + subdep_name + '</li>'
            chart_edges.append({'source': name, 'target': subdep_name})
        subdeps += '</ul>'
        
        html_dep_table_rows += f"""
            <tr>
                <td>{name}</td>
                <td>{version}</td>
                <td>{licenses}</td>
                <td><a href='{purl}' target='_blank'>{purl}</a></td>
                <td>{subdeps}</td>
            </tr>
        """

    # Generate chart data for report
    html_chart_data = ''
    for edge in chart_edges:
        html_chart_data += "{'source':'" + edge['source'] + "', 'target':'" + edge['target'] + "', 'value':'1'},\n"
    
    # Replace data in report template
    html_content = html_content.replace('{{app_name}}', app_name)
    html_content = html_content.replace('{{app_version}}', app_version)
    html_content = html_content.replace('{{summary}}', summary)
    html_content = html_content.replace('{{scan_time}}', scan_time)
    html_content = html_content.replace('{{html_dep_table_rows}}', html_dep_table_rows)
    html_content = html_content.replace('{{html_chart_data}}', html_chart_data)
    
    # Write report
    with open(output_html, 'w') as file:
        file.write(html_content)
    return True
